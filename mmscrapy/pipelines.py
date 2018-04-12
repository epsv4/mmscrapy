# coding=utf-8
import logging
import datetime
import json
from .model import getSession, ImageList
from sqlalchemy.orm.session import Session
from pymysql.err import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from .items import ImageListItem, PageListItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


session: Session = getSession()


class MmscrapyPipeline(object):
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # print("===========================")
        if type(item) is PageListItem:
            count = item["count"]
            urls = item["urls"]
            names = item["names"]
            now = datetime.datetime.now()
            logging.debug("urls=%s", str(urls))
            ms = [ImageList(kind=1, name=names[i], url=urls[i], createdt=now, modifydt=now, favourite='0' * 100)
                for i in range(count)]
            for m in ms:
                try:
                    session.query(ImageList).filter(ImageList.url == m.url).one()
                except NoResultFound:
                    session.add(m)
            session.commit()
        elif type(item) is ImageListItem:
            count = item["count"]
            father_url = item["father_url"]
            urls = item["urls"]
            try:
                il = session.query(ImageList).filter(ImageList.url == father_url).one()
            except NoResultFound:
                pass
            else:
                obj = json.loads(il.json)
                if "urls" in obj:
                    old_urls = set(obj["urls"])
                else:
                    old_urls = set()
                new_urls = old_urls.union(urls)
                obj["urls"] = list(new_urls)
                il.json = json.dumps(obj)
                session.add(il)
                session.commit()
        return item
