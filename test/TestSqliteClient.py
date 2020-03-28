# coding: utf-8
"""
------------------------------------------------------------
   File Name: TestSqliteClient.py
   Description: Sqlite Client operation test
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Has already finished Sqlite Client operation test
------------------------------------------------------------
"""
__author__ = 'JockMing'
from db.SqliteClient import SqliteClient
from exception.BaseException import ConDbFail

try:
    sqlite_cli = SqliteClient()
    sqlite_cli.init_db()
except Exception:
    raise ConDbFail

proxy = {'ip': '192.168.1.3', 'port': int('8080'), 'types': 0, 'protocol': 0,
         'country': u'中国', 'area': u'四川', 'speed': 0}
sqlite_cli.insert(proxy)
print(sqlite_cli.select(5))
sqlite_cli.close_db()
