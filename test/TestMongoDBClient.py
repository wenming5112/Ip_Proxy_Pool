# coding: utf-8
"""
------------------------------------------------------------
   File Name: TestMongoDBClient.py
   Description: MongoDB Client operation test
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Has already finished MongoDB Client operation test
------------------------------------------------------------
"""
__author__ = 'JockMing'
from db.MongoDbClient import MongoDBClient
from exception.BaseException import ConDbFail

try:
    client = MongoDBClient()
    client.init_db()
except BaseException as e:
    print(e.__cause__)
    raise ConDbFail

proxy = {'ip': '192.168.1.2', 'port': 80, 'type': 0, 'protocol': 0,
         'country': '中国', 'area': '广州', 'speed': 11.123, 'types': ''}
client.init_db()
client.insert(proxy)
re = client.select(3, {'types': "", 'protocol': 0})
print(re)
client.close_db()
