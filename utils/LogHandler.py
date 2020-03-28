# coding: utf-8
"""
------------------------------------------------------------
   File Name: LogHandler.py
   Description: Log operation module
   Author: JHao
   date: 2017/03/06
------------------------------------------------------------
   Change Activity:
                   2017/03/06: Log handler
                   2017/09/21: Screen output/file output optional (default screen and file output)
------------------------------------------------------------
"""
__author__ = 'JHao'

import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Log level
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class LogHandler(logging.Logger):
    """
    LogHandler
    """

    def __init__(self, name, level=DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        Set file handler
        :param level: level default None
        """
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        Set stream handler
        :param level: level
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def reset_name(self, name):
        """
        Reset name
        :param name: name
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()


class Logger(object):
    log_handler = LogHandler('Ip_Proxy_Pool_Logs')


if __name__ == '__main__':
    log = Logger()
    log = log.log_handler
    log.info('this is a test msg')
    log.error("bad error")
