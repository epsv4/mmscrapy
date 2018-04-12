import os
import sqlalchemy
import logging
import scrapy
import pybloom_live
import atexit
import sys
import re
import json
import datetime
from ..init import init
from scrapy.http import Request, Response
from ..model import ImageList, getSession
from ..items import PageListItem, ImageListItem
from scrapy.spiders import CrawlSpider

init()
NUMBER_PATTERN = re.compile('.*?(\d+)')
# a = Response()
# a.meta


class MM131Spider(CrawlSpider):
    name = "mm131"
    allowed_domains = ["http://m.mm131.com"]
    start_urls = [
        "http://m.mm131.com/more.php?page=1"
    ]

    def start_requests(self):
        session = getSession()
        if 0:
            for page in range(2664, 2665):
                yield Request(url='http://m.mm131.com/more.php?page=%d' % page,
                              callback=self.parseList)
        elif 1:
            for page in range(2000, 5000):
                yield Request(url='http://www.mm131.com/xinggan/%d.html' % page,
                              callback=self.parseListI)
        else:
            for il in session.query(ImageList).filter(ImageList.id >= 94):
                yield Request(url=il.url, meta={"father_url": il.url}, callback=self.parseListI)
                # break

    def parseList(self, response: scrapy.http.response.html.HtmlResponse):
        pass

    def parseListI(self, response: scrapy.http.response.html.HtmlResponse):
        print('$$$$$$$$$${}'.format(response.url))
        title = response.xpath(
            '//div[@class="content"]/h5').xpath('text()')[0].extract()
        selectors = response.xpath('//span[@class="page-ch"]')
        n = 0
        for sel in selectors:
            text = sel.xpath('text()')[0].extract()
            if text.find('共') >= 0:
                n = int(re.match(NUMBER_PATTERN, text).group(1))
        if n == 0:
            return
        session: sqlalchemy.orm.session.Session = getSession()
        now = datetime.datetime.now()
        url = response.url
        uid = re.search(NUMBER_PATTERN, url[url.rfind('/'):]).group(1)
        try:
            imageList: ImageList = session.query(ImageList).filter(
                ImageList.url == response.url).one()
            logging.info('--------------------')
            logging.info(imageList.url)
            session.delete(imageList)
        except Exception as e:
            pass
        session.add(ImageList(kind=2, name=title,
                              url=response.url, created_at=now, updated_at=now, json=json.dumps({
                                  "urls": ["http://img1.mm131.me/pic/%s/%d.jpg" % (uid, i) for i in range(n)]
                              }
                              )))
        session.commit()


if __name__ == "__main__":
    print(os.getcwd())
    if not os.path.exists("bloom.bin"):
        bloom = pybloom_live.BloomFilter(100000, 0.0001)
    else:
        with open("bloom.bin", "rb") as fd:
            bloom = pybloom_live.BloomFilter.fromfile(fd)
    if not "123" in bloom:
        bloom.add("123")
    else:
        logging.debug("already in")
    fw = open("bloom.bin", "wb")
    bloom.tofile(fw)
    fw.close()
