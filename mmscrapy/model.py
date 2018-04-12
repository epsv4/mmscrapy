# coding=utf8
from sqlalchemy import Column, VARCHAR, Integer, Float, SmallInteger, String, DateTime
from sqlalchemy import CHAR, DECIMAL, UniqueConstraint, Index, TEXT
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


def getBase():
    return BASE


def getSession():
    global DBSession
    return DBSession()


def initDb():
    global DBSession
    engine = create_engine(
        "mysql+pymysql://root:111aaa@127.0.0.1/test?charset=utf8")
    DBSession = sessionmaker(bind=engine)
    BASE.metadata.create_all(engine)

class Simple(BASE):
    __tablename__ = 'simple'
    id = Column(Integer, primary_key=True)


class ImageList(BASE):
    __tablename__ = 't_imagelists'

    id = Column(Integer, primary_key=True)
    kind = Column(Integer)
    name = Column(String(200))
    description = Column(String(200))
    url = Column(String(200))
    created_at = Column(DateTime, )
    updated_at = Column(DateTime)
    status = Column(CHAR(4))
    json = Column(VARCHAR(10000))
    favourite = Column(VARCHAR(100))

    __table_args__ = (
        UniqueConstraint('url', name='uix_url'),  # 鑱斿悎鍞竴绱㈠紩
        # Index('ix_id_name', 'name', 'extra'),  # 鑱斿悎绱㈠紩
        # Index("ix_name_extra", "name", "extra"),
    )

    def __repr__(self):
        return "<ImageList(id='%d', name='%s')>" % (self.id, self.name)

class News(BASE):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    url = Column(String(200))
    title = Column(String(200))
    content = Column(String(10000))
    created_at = Column(DateTime, )
    updated_at = Column(DateTime)


    def __repr__(self):
        return "<News(id='%d', title='%s')>" % (self.id, self.title)


class ImageInfo(BASE):
    __tablename__ = 't_imageinfo'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(200))
    url = Column(String(200))
    createdt = Column(DateTime)
    modifydt = Column(DateTime)
    status = Column(CHAR(4))
    json = Column(TEXT)

    __table_args__ = (
        UniqueConstraint('url', name='uix_url'),  # 鑱斿悎鍞竴绱㈠紩
        # Index('ix_id_name', 'name', 'extra'),  # 鑱斿悎绱㈠紩
        # Index("ix_name_extra", "name", "extra"),
    )

    def __repr__(self):
        return "<ImageList(id='%d', name='%s')>" % (self.id, self.name)

__all__ = ["getSession", "initDb", "ImageList", "Simple"]
