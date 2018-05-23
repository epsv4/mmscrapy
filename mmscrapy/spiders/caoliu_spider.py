import os
import sqlalchemy
import logging
import scrapy
import pybloom_live
import atexit
import sys
import re
import json
import time
import datetime
from typing import List
from ..init import init
from scrapy.http import Request, Response
from ..model import ImageList, getSession
from ..items import PageListItem, ImageListItem
from scrapy.spiders import CrawlSpider
from sqlalchemy.orm.exc import NoResultFound
from traceback import format_exc

init()
NUMBER_PATTERN = re.compile('.*?(\d+)')
# a = Response()
# a.meta

BASE_URL = "http://cl.v4tg.pw"


class CaoliuSpider(CrawlSpider):
    name = "caoliu"
    allowed_domains = [BASE_URL]
    start_urls = [
        "http://m.mm131.com/more.php?page=1"
    ]
    maxNPage = 100
    currentPage = 0

    def start_requests(self):
        session = getSession()
        yield Request('%s/thread0806.php?fid=8&search=&page=1' % BASE_URL,
                      callback=self.parseListI)

    def parseListII(self, response: scrapy.http.response.html.HtmlResponse):
        print('parseListII .........')
        url = response.url
        session: sqlalchemy.orm.session.Session = getSession()
        try:
            imageList: ImageList = session.query(ImageList).filter(
                ImageList.url == url).one()
        except NoResultFound as e:
            logging.info("NoResultFound")
            pass
        else:
            jsnStr = imageList.json
            jsnObj = json.loads(jsnStr)
            urls = jsnObj.get('urls', [])
            if len(urls) != 0:
                return
            try:
                imgs = [i.xpath('@data-src')[0].extract()
                        for i in response.css('div.tpc_content input')]
            except:
                imgs = [i.xpath('@src')[0].extract()
                        for i in response.css('div.tpc_content input')]
            urlsSet = set(urls)
            for img in imgs:
                urlsSet.add(img)
            jsnObj["urls"] = list(urlsSet)
            imageList.json = json.dumps(jsnObj)
            session.add(imageList)
            session.commit()

    def parseListI(self, response: scrapy.http.response.html.HtmlResponse):
        if self.currentPage == self.maxNPage:
            return
        self.currentPage += 1
        ax = response.css('#ajaxtable > tbody > tr  > td.tal > h3 > a')
        session: sqlalchemy.orm.session.Session = getSession()
        now = datetime.datetime.now()
        for a in ax:
            try:
                title = a.xpath('text()')[0].extract()
                href = a.xpath('@href')[0].extract()
                url = "%s/%s" % (BASE_URL, href)
                print('%s %s %s' % (title, href, url))
                if href.find('htm_data/8') < 0:
                    continue
                try:
                    imageList: ImageList = session.query(ImageList).filter(
                        ImageList.url == url).one()
                    jsnObj = json.loads(imageList.json)
                    if 'urls' in jsonObj and len(jsnObj["urls"]) != 0:
                        continue
                    yield Request(url, callback=self.parseListII,
                                  dont_filter=True, priority=1)
                except NoResultFound as e:
                    logging.info('no result found')
                    session.add(ImageList(kind=4, name=title, url=url, favourite='0'*100,
                                          created_at=now, updated_at=now, json='{}'))
                    session.commit()
                    yield Request(url, callback=self.parseListII,
                                  dont_filter=True, priority=1)
            except Exception as e:
                logging.error(format_exc())
                continue
        time.sleep(1)
        for i in response.css('div.pages a'):
            logging.info('================ %s', str(i))
            tmp = i.xpath('text()').extract()
            logging.debug('>>>>>>>>> %s', str(tmp))
            if len(tmp) != 0 and tmp[0] == '下一頁':
                yield Request('%s/%s' % (BASE_URL, i.xpath('@href').extract()[0]), callback=self.parseListI,
                              dont_filter=True)
            else:
                continue


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
