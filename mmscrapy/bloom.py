import sys
import os
import pybloom_live
import logging


class Bloom(object):
    _bloomSavePath = os.path.join(os.path.dirname(__file__), "bloom.bin")
    _bloom: pybloom_live.BloomFilter
    print(_bloomSavePath)

    @staticmethod
    def init():
        if not os.path.exists(Bloom._bloomSavePath):
            bloom = pybloom_live.BloomFilter(100000, 0.0001)
        else:
            with open(Bloom._bloomSavePath, "rb") as fd:
                bloom = pybloom_live.BloomFilter.fromfile(fd)
        Bloom._bloom = bloom
        # print(Bloom._bloom)

    @staticmethod
    def deinit():
        # print(Bloom._bloom)
        fw = open(Bloom._bloomSavePath, "wb")
        Bloom._bloom.tofile(fw)
        fw.close()

    @staticmethod
    def add(key):
        Bloom._bloom.add(key)

    @staticmethod
    def hasKey(key):
        return key in Bloom._bloom
