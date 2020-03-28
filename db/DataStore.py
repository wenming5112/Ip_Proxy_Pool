# coding:utf-8
"""
------------------------------------------------------------
   File Name: DataStore.py
   Description: Database operation class
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Database operation class
------------------------------------------------------------
"""
from common.config import DB_CONFIG
from exception.BaseException import ConDbFail
from utils.LogHandler import Logger

log = Logger.log_handler

try:
    if DB_CONFIG['DB_CONNECT_TYPE'] == "sqlite":
        from db.SqliteClient import SqliteClient as SqlHelper
    elif DB_CONFIG['DB_CONNECT_TYPE'] == "mongodb":
        from db.MongoDbClient import MongoDBClient as SqlHelper
    elif DB_CONFIG['DB_CONNECT_TYPE'] == "redis":
        from db.RedisClient import RedisClient as SqlHelper
    elif DB_CONFIG['DB_CONNECT_TYPE'] == "mysql":
        from db.MysqlClient import MysqlClient as SqlHelper
    else:
        raise ConDbFail("Unsupported database type")
    sql_helper = SqlHelper()
    sql_helper.init_db()
except Exception as e:
    raise ConDbFail


def store_data(queue2, db_proxy_num):
    """
    Read the data in the queue and write it to the database
    :param queue2: queue2
    :param db_proxy_num:
    """
    success_num = 0
    fail_num = 0
    while True:
        try:
            proxy = queue2.get(timeout=300)
            if proxy:
                sql_helper.insert(proxy)
                success_num += 1
            else:
                fail_num += 1
            log.info('Ip_Proxy_Pool ------>>>>>> Success ip num :%d,Fail ip num:%d' % (success_num, fail_num))
        except ConDbFail as ex:
            log.error(ex.__str__())
            if db_proxy_num.value != 0:
                success_num += db_proxy_num.value
                db_proxy_num.value = 0
                success_num = 0
                fail_num = 0
