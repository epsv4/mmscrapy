# coding=utf8
import atexit
import logging
logging.basicConfig(level=logging.DEBUG, 
    format='%(filename)20s %(lineno)04d %(message)s')
from .model import initDb
from .bloom import Bloom


def init():
    Bloom.init()
    initDb()


def exitFunc():
    Bloom.deinit()


atexit.register(exitFunc)

__all__ = []

if __name__ == "__main__":
    pass
