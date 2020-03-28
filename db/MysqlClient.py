#!/usr/bin/env python
# coding: utf-8
from sqlalchemy.orm import sessionmaker

from common.config import DB_CONFIG
from db.SqliteClient import SqliteClient
from model.Proxy import Proxy

__author__ = 'JockMing'

from sqlalchemy import create_engine


class MysqlClient(SqliteClient):
    params = {"ip": Proxy.ip, "port": Proxy.port, "types": Proxy.types, "protocol": Proxy.protocol,
              "country": Proxy.country, "area": Proxy.area, "score": Proxy.score}

    def __init__(self):
        super(SqliteClient, self).__init__()
        self.engine = create_engine(DB_CONFIG["DB_CONNECT_STRING"], echo=False, encoding="utf-8")
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()


if __name__ == '__main__':
    mysql_client = MysqlClient()
    mysql_client.init_db()
    proxy = {'ip': '192.168.1.1', 'port': 80, 'types': 0, 'protocol': 0,
             'country': 'cn', 'area': 'guangzhou', 'speed': 11.123}
    # d = mysql_client.insert(proxy)
    # print("新增结果返回", d)
    # re_up = mysql_client.update({'ip': '192.168.1.1', 'port': 80}, {'score': 13})
    # print("是否修改成功", re_up)
    # returned a tuple
    data = mysql_client.select(3)
    print("query data: ", data, " data type: ", type(data))
    mysql_client.close_db()
