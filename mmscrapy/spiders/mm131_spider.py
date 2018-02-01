import os
import sqlalchemy
import logging
import scrapy
import pybloom_live
import atexit
import sys
import datetime
from ..init import init
from scrapy.http import Request, Response
from ..model import ImageList, getSession
from ..items import PageListItem, ImageListItem
from scrapy.spiders import CrawlSpider

init()

# a = Response()
# a.meta

class MM131Spider(CrawlSpider):
    name = "mm131"
    allowed_domains = ["http://m.mm131.com"]
    start_urls = [
        "http://m.mm131.com/more.php?page=1"
    ]

    def start_requests(self):
        session  = getSession()
        if 1:
            for page in range(1, 2):
                yield Request(url='http://m.mm131.com/more.php?page=%d' % page, 
                callback=self.parseList)
        else:
            for il in session.query(ImageList).filter(ImageList.id >= 94):
                yield Request(url=il.url, meta={"father_url": il.url}, callback=self.parseListI)
                # break

    def parseList(self, response):
        selectors = response.xpath('//article/div')
        urls = []
        names = []
        item = PageListItem()
        n = 0
        for sel in selectors:
            logging.debug("xxxxxxxxxxxxxxxxxx")
            logging.debug(sel)
            a = sel.xpath('h2/a')
            href, name = a.xpath('@href').extract()[0], \
                a.xpath('text()').extract()[0]
            urls.append(href)
            names.append(name)
        item["urls"] = urls
        item["names"] = names
        item["count"] = len(urls)
        item["kind"] = 2
        yield item

    def parseListI(self, response : Response):
        # response.meta
        logging.debug("meta=======================" + str(response.meta))
        figure = response.xpath('//div[@class="place-padding"]/figure')
        urls = figure.xpath('//img[contains(@src, ".jpg")]/@src').extract()
        imageListItem = ImageListItem()
        imageListItem["count"] = len(urls)
        imageListItem["father_url"] = response.meta["father_url"]
        imageListItem["urls"] = urls
        yield imageListItem
        try:
            nextPageUrl = response.xpath(
                '//a[text()="下一页"]/@href').extract()[0]
        except IndexError:
            pass
        else:
            logging.debug("开始获取下一页============" + nextPageUrl)
            yield Request(url=nextPageUrl, meta=response.meta,
                          callback=self.parseListI, dont_filter=True)


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
