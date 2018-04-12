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
from ..model import getSession, News
from ..items import PageListItem, ImageListItem
from scrapy.spiders import CrawlSpider
from sqlalchemy.orm.exc import NoResultFound
from traceback import format_exc

init()
NUMBER_PATTERN = re.compile('.*?(\d+)')
# a = Response()
# a.meta



class VoaSpider(CrawlSpider):
    name = "voa"
    allowed_domains = ["http://www.51voa.com"]
    start_urls = [
        "http://www.51voa.com/VOA_Standard_English"
    ]
    maxNPage = 3
    BASE_URL = 'http://www.51voa.com'

    def start_requests(self):
        session = getSession()
        yield Request('http://www.51voa.com/VOA_Standard_English',
                      callback=self.parseListI)

    def parseListII(self, response: scrapy.http.response.html.HtmlResponse):
        print('parseListII .........')
        url = response.url
        session: sqlalchemy.orm.session.Session = getSession()
        try:
            px = response.css('#content > p')
            ps = []
            for p in px:
                ps.append(p.xpath('text()')[0].extract())
            session
            # session.execute('update news set content = ? where url = ?', ['\n'.join(ps), url])
            session.query(News).filter(News.url == url).update({"content" : '\n'.join(ps)})
            session.commit()
        except Exception:
            logging.error(format_exc())
            

    def parseListI(self, response: scrapy.http.response.html.HtmlResponse):
        ax = response.css('#list > ul > li > a')
        session: sqlalchemy.orm.session.Session = getSession()
        now = datetime.datetime.now()
        for a in ax:
            try:
                title = a.xpath('text()')[0].extract()
                href = a.xpath('@href')[0].extract()
                url = "%s/%s" % (VoaSpider.BASE_URL, href)
                print('%s %s %s' % (title, href, url))
                try:
                    news: News = session.query(News).filter(
                        News.url == url).one()
                    yield Request(url, callback=self.parseListII,
                                  dont_filter=True, priority=1)
                except NoResultFound as e:
                    logging.info('no result found')
                    session.add(News(url=url, title=title, created_at=now, updated_at=now))
                    session.commit()
                    yield Request(url, callback=self.parseListII,
                                  dont_filter=True, priority=1)
            except Exception as e:
                logging.error(format_exc())
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
