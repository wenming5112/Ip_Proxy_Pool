# coding:utf-8
"""
------------------------------------------------------------
   File Name: BaseException.py
   Description: Custom exception
   Author: JockMing
   Date: 22020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Custom exception
------------------------------------------------------------
"""
import common.config as config

__author__ = 'JockMing'


class TestUrlFail(BaseException):
    def __str__(self):
        return "Access to %s failed, please check the network connection" % config.TEST_IP


class ConDbFail(BaseException):
    def __str__(self):
        s = config.DB_CONFIG.get("DB_CONNECT_STRING", {})
        return "Use DB_CONNECT_STRING: %s -- connection to database failed" % s


class CrawlerException(Exception):
    def __init__(self, message=None, doc=None):
        self.message = message
        self.__doc__ = doc

    def __str__(self):
        return str(self.message)


if __name__ == '__main__':
    print(config.DB_CONFIG.get("DB_CONNECT_STRING", {}))
    try:
        raise CrawlerException("自定义异常")
    except Exception as e:
        print(e)
        print(e.__doc__)
        print(e.__str__())
        print(e.__class__)
