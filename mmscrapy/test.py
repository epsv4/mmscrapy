import sqlalchemy
from model import *


def test1():
    session = getSession()
    print(ImageList)
    il = session.query(ImageList).one()


if __name__ == "__main__":
    initDb()
    session : sqlalchemy.orm.session.Session = getSession()
    simple = session.query(Simple).filter(Simple.id == 1).one()
    print(simple.id)
    session.delete(simple)
    session.commit()
