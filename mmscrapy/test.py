from .model import *

def test1():
    session = getSession()
    print(ImageList)
    il = session.query(ImageList).one()

if __name__ == "__main__":
    session = getSession()