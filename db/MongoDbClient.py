# coding:utf-8
"""
------------------------------------------------------------
   File Name: MongoDbClient.py
   Description: MongoDB Client operation implementation
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: This is MongoDB Client operation implementation and  has already finished the test
------------------------------------------------------------
"""

__author__ = 'JockMing'
import pymongo

from common.config import DB_CONFIG, DEFAULT_SCORE
from db.InterfaceDb import InterfaceDb


class MongoDBClient(InterfaceDb):
    def __init__(self):

        self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'], connect=False)
        self.__mongo_db = None
        self.__mongo_collection = None

    def init_db(self):
        self.__mongo_db = self.client["proxy"]
        self.__mongo_collection = self.__mongo_db["ip_pool"]

    def drop_db(self):
        self.client.drop_database(self.__mongo_db)

    def insert(self, value=None):
        if value:
            proxy_from_spider = dict(ip=value["ip"], port=value["port"], types=value["types"],
                                     protocol=value["protocol"], country=value["country"],
                                     area=value["area"], speed=value["speed"], score=DEFAULT_SCORE)
            self.__mongo_collection.insert_one(proxy_from_spider)

    def delete(self, conditions=None):
        if conditions:
            self.__mongo_collection.remove(conditions)
            return {"delete_num": "ok"}
        else:
            return {"delete_num": "fail"}

    def update(self, conditions=None, value=None):
        # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
        if conditions and value:
            self.__mongo_collection.update(conditions, {"$set": value})
            return {'update_num': 'ok'}
        else:
            return {'update_num': 'fail'}

    def select(self, count=None, conditions=None):
        if count:
            count = int(count)
        else:
            count = 0
        if conditions:
            conditions = dict(conditions)
            if 'count' in conditions:
                del conditions['count']
            conditions_name = ['types', 'protocol']
            for condition_name in conditions_name:
                var = condition_name
                value = conditions[var]
                if value:
                    conditions[condition_name] = int(value)
        else:
            conditions = {}
        items = self.__mongo_collection.find(conditions, limit=count).sort(
            [("speed", pymongo.ASCENDING), ("score", pymongo.DESCENDING)])
        results = []
        for item in items:
            result = {"ip": item['ip'], "port": item['port'], "score": item['score']}
            results.append(result)
        return results

    def close_db(self):
        self.client.close()


if __name__ == '__main__':
    # Test the MongoDB client
    client = MongoDBClient()
    proxy = {'ip': '192.168.1.2', 'port': 80, 'type': 0, 'protocol': 0,
             'country': '中国', 'area': '广州', 'speed': 11.123, 'types': ''}
    client.init_db()
    # client.insert(proxy)
    re = client.select(3, {'types': "", 'protocol': 0})
    print(re)
    client.close_db()
