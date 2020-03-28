# coding: utf-8
"""
------------------------------------------------------------
   File Name: TestLogHandler.py
   Description: Log operation test
   Author: JHao
   date: 2017/03/06
------------------------------------------------------------
   Change Activity:
                   2017/03/06: Log handler test
                   2017/09/21: Screen output/file output optional (default screen and file output)
------------------------------------------------------------
"""
__author__ = 'JHao'
from utils.LogHandler import LogHandler

log = LogHandler("log_test")
log.info("test_log_info")
