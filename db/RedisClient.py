# coding: utf-8
# from __future__ import absolute_import, unicode_literals

"""
------------------------------------------------------------
   File Name: RedisClient.py
   Description: Redis Client operation implementation
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Redis Client operation implementation
------------------------------------------------------------
"""
__author__ = 'JockMing'

import redis
import common.config as config
from db.InterfaceDb import InterfaceDb
from model.Proxy import Proxy


class RedisClient(InterfaceDb):
    def __init__(self, url=None):
        self.index_names = ('types', 'protocol', 'country', 'area', 'score')
        self.redis_url = url or config.DB_CONFIG['DB_CONNECT_STRING']
        self.__redis_conn = None
        self.__pool = None

    def init_db(self, url=None):
        self.__pool = redis.ConnectionPool.from_url(url or self.redis_url)
        self.__redis_conn = redis.StrictRedis(connection_pool=self.__pool)

    def drop_db(self):
        return self.__redis_conn.flushdb()

    @staticmethod
    def get_proxy_name(ip=None, port=None, protocol=None, proxy=None):
        ip = ip or proxy.ip
        port = port or proxy.port
        protocol = protocol or proxy.protocol
        return "proxy::{}:{}:{}".format(ip, port, protocol)

    @staticmethod
    def get_index_name(index_name, value=None):
        if index_name == 'score':
            return 'index::score'
        return "index::{}:{}".format(index_name, value)

    def get_proxy_by_name(self, name):
        pd = self.__redis_conn.hgetall(name)
        if pd:
            return Proxy(**{k.decode('utf8'): v.decode('utf8') for k, v in pd.items()})

    def get_keys(self, conditions):
        select_keys = {self.get_index_name(key, conditions[key]) for key in conditions.keys() if
                       key in self.index_names}
        if 'ip' in conditions and 'port' in conditions:
            return self.__redis_conn.keys(self.get_proxy_name(conditions['ip'], conditions['port'], '*'))
        if select_keys:
            return [name.decode('utf8') for name in self.__redis_conn.sinter(keys=select_keys)]
        return []

    def insert(self, value=None):
        proxy = Proxy(ip=value['ip'], port=value['port'], types=value['types'], protocol=value['protocol'],
                      country=value['country'], area=value['area'],
                      speed=value['speed'], score=value.get('score', config.DEFAULT_SCORE))
        mapping = proxy.__dict__
        for k in list(mapping.keys()):
            if k.startswith('_'):
                mapping.pop(k)
        object_name = self.get_proxy_name(proxy=proxy)
        # 存结构
        insert_num = self.__redis_conn.hmset(object_name, mapping)
        # 创建索引
        if insert_num > 0:
            for index_name in self.index_names:
                self.create_index(index_name, object_name, proxy)
        return insert_num

    def create_index(self, index_name, object_name, proxy):
        redis_key = self.get_index_name(index_name, getattr(proxy, index_name))
        if index_name == 'score':
            return self.__redis_conn.zadd(redis_key, object_name, int(proxy.score))
        return self.__redis_conn.sadd(redis_key, object_name)

    def delete(self, conditions=None):
        proxy_keys = self.get_keys(conditions)
        index_keys = self.__redis_conn.keys(u"index::*")
        if not proxy_keys:
            return 0

        for key in index_keys:
            if key == b'index::score':
                self.__redis_conn.zrem(self.get_index_name('score'), *proxy_keys)
            else:
                self.__redis_conn.srem(key, *proxy_keys)
        return self.__redis_conn.delete(*proxy_keys) if proxy_keys else 0

    def update(self, conditions=None, values=None):
        objects = self.get_keys(conditions)
        count = 0
        for name in objects:
            for k, v in values.items():
                if k == 'score':
                    self.__redis_conn.zrem(self.get_index_name('score'), [name])
                    self.__redis_conn.zadd(self.get_index_name('score'), name, int(v))
                self.__redis_conn.hset(name, key=k, value=v)
            count += 1
        return count

    def select(self, count=None, conditions=None):
        count = (count and int(count)) or 1000  # 最多返回1000条数据
        count = 1000 if count > 1000 else count

        query = {k: v for k, v in conditions.items() if k in self.index_names} if conditions else None
        if query:
            objects = list(self.get_keys(query))[:count]
            redis_name = self.get_index_name('score')
            objects.sort(key=lambda x: int(self.__redis_conn.zscore(redis_name, x)))
        else:
            objects = list(
                self.__redis_conn.zrevrangebyscore(self.get_index_name("score"), '+inf', '-inf', start=0, num=count))

        result = []
        for name in objects:
            p = self.get_proxy_by_name(name)
            result.append((p.ip, p.port, p.score))
        return result


# There are still problems
if __name__ == '__main__':
    client = RedisClient()
    client.init_db('redis://:123456@127.0.0.1:6379/8?decode_responses=True')
    proxy1 = {'ip': '192.168.1.1', 'port': 80, 'type': 0, 'protocol': 0,
              'country': '中国', 'area': '广州', 'speed': 11.123, 'types': 1}
    proxy2 = {'ip': 'localhost', 'port': 433, 'type': 1, 'protocol': 1,
              'country': u'中国', 'area': u'广州', 'speed': 123, 'types': 0, 'score': 100}


    # assert client.insert(proxy1) is True
    # assert client.insert(proxy2) is True
    # assert client.get_keys({'types': 1}) == ['proxy::192.168.1.1:80:0', ], client.get_keys({'types': 1})
    # assert client.select(conditions={'protocol': 0}) == [('192.168.1.1', '80', '0')]
    # assert client.update({'types': 1}, {'score': 888}) == 1
    # assert client.select() == [('192.168.1.1', '80', '888'), ('localhost', '433', '100')]
    # assert client.delete({'types': 1}) == 1
    # client.drop_db()
