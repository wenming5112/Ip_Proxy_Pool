# coding:utf-8
"""
------------------------------------------------------------
   File Name: SqliteClient.py
   Description: Sqlite Client operation implementation
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Sqlite Client operation implementation
------------------------------------------------------------
"""
__author__ = 'JockMing'

import datetime
import decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util._collections import AbstractKeyedTuple

from common.config import DB_CONFIG
from db.InterfaceDb import InterfaceDb
from model.Proxy import Proxy, BaseModel

format_ymd_hms = "%Y-%m-%d %H:%M:%S"


class SqliteClient(InterfaceDb):
    params = {"ip": Proxy.ip, "port": Proxy.port, "types": Proxy.types, "protocol": Proxy.protocol,
              "country": Proxy.country, "area": Proxy.area, "score": Proxy.score}

    def __init__(self):
        connect_args = {"check_same_thread": False}
        self.engine = create_engine(DB_CONFIG["DB_CONNECT_STRING"], echo=False, connect_args=connect_args)
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()
        # Open auto commit
        # self.__session.autocommit = True

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)

    def close_db(self):
        self.session.close()

    def insert(self, value=None):
        """
        The new data
        :param value: a dict include ip,port,types...
        :return: add_num
        """
        in_proxy = Proxy(ip=value['ip'], port=value['port'], types=value['types'],
                         protocol=value['protocol'], country=value['country'],
                         area=value['area'], speed=value['speed'])
        # Use to determine if new success is added
        add_num = self.session.add(in_proxy)
        self.session.commit()
        return {"add_num": add_num}

    def delete(self, search_keys=None):
        """
        delete the data
        :param search_keys: search_keys
        :return: delete_num
        """
        if search_keys:
            search_key_list = []
            for key in list(search_keys.keys()):
                if self.params.get(key, None):
                    search_key_list.append(self.params.get(key) == search_keys.get(key))
            search_keys = search_key_list
            query = self.session.query(Proxy)
            for search_key in search_keys:
                query = query.filter(search_key)
            delete_num = query.delete()
            self.session.commit()
        else:
            delete_num = 0
        return {'delete_num': delete_num}

    def update(self, search_keys=None, value=None):
        """
        update the data
        :param search_keys: search_keys
        :param value: a dict like：{'ip':192.168.0.1}
        :return: dict: update_num
        """
        if search_keys and value:
            search_key_list = []
            for key in list(search_keys.keys()):
                if self.params.get(key, None):
                    search_key_list.append(self.params.get(key) == search_keys.get(key))
            search_keys = search_key_list
            query = self.session.query(Proxy)
            for search_key in search_keys:
                query = query.filter(search_key)
            update_value = {}
            for key in list(value.keys()):
                if self.params.get(key, None):
                    update_value[self.params.get(key, None)] = value.get(key)
            update_num = query.update(update_value)
            self.session.commit()
        else:
            update_num = 0
        return {'update_num': update_num}

    def select(self, count=None, search_keys=None):
        """
        Query data
        :param count: Query how many records
        :param search_keys: The type of conditions is a dictionary like "self.params"
        :return:
        """
        if search_keys:
            search_key_list = []
            for key in list(search_keys.keys()):
                if self.params.get(key, None):
                    search_key_list.append(self.params.get(key) == search_keys.get(key))
            search_keys = search_key_list
        else:
            search_keys = []
        query = self.session.query(Proxy.ip, Proxy.port, Proxy.score)
        if len(search_keys) > 0 and count:
            for search_key in search_keys:
                # Filter based on query criteria
                query = query.filter(search_key)
            return db_datalist_to_dict(query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all())
        elif count:
            return db_datalist_to_dict(query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all())
        elif len(search_keys) > 0:
            for search_key in search_keys:
                query = query.filter(search_key)
            # Sort by score and speed
            return db_datalist_to_dict(query.order_by(Proxy.score.desc(), Proxy.speed).all())
        else:
            return db_datalist_to_dict(query.order_by(Proxy.score.desc(), Proxy.speed).all())


def db_datalist_to_dict(res_obj):
    """
    AbstractKeyedTuple  This data type is returned when certain fields are returned
    TTDModel is the parent class of the custom Sqlalchemy class, in which the to ˊ dict() function is overridden to control the output
    isinstance(obj,class)Judge whether obj is a class or its subclass, return true if it is not, return false if it is not
    db return list to dict
    :param res_obj:
    :return:
    """
    if not res_obj:
        return None
    # parse list
    if isinstance(res_obj, list):
        if len(res_obj) == 0:
            return None
        if isinstance(res_obj[0], AbstractKeyedTuple):
            dic_list = datalist_format([dict(zip(result.keys(), result)) for result in res_obj])
            if dic_list:
                for item in dic_list:
                    for key in item.keys():
                        if key.find("Id") >= 0 or key.find("uuid") >= 0 or key.find("_id") >= 0:
                            item[key] = str(item[key])
            return dic_list
        elif isinstance(res_obj[0], Proxy):
            [item.__dict__.pop("_sa_instance_state") for item in res_obj]
            return datalist_format([item.__dict__ for item in res_obj])
        elif isinstance(res_obj[0], dict):  # 在db中存在json字段时返回的是dict
            return datalist_format(res_obj)
        else:
            return None
    else:
        return db_data_to_dict(res_obj)


def db_data_to_dict(res_obj):
    """
    Database returns single data to Dict
    :param res_obj:
    :return: dict
    """
    if not res_obj:
        return None
    if isinstance(res_obj, dict):
        return res_obj
    elif isinstance(res_obj, AbstractKeyedTuple):
        # Turn into a dictionary
        dict_obj = data_format(dict(zip(res_obj.keys(), res_obj)))
        # Turn null into an empty string
        if res_obj and len(res_obj.keys()) > 0:
            for key in res_obj.keys():
                if not dict_obj[key]:
                    dict_obj[key] = ""
                if key.find("Id") >= 0 or key.find("uuid") >= 0 or key.find("_id") >= 0:
                    dict_obj[key] = str(dict_obj[key])

        return dict_obj
    elif isinstance(res_obj, Proxy):
        res_obj.__dict__.pop("_sa_instance_state")
        return data_format(res_obj.__dict__)
    else:
        return None


def datalist_format(res_list):
    """
    Transfer from datetime.datetime to [2018:12:12 10:10:56]
    :param res_list: returned list
    :return: list
    """
    if not res_list or not isinstance(res_list, list):
        return res_list
    for item in res_list:
        for key in item.keys():
            if isinstance(item[key], datetime.datetime) \
                    or isinstance(item[key], datetime.date):
                item[key] = str(item[key])
            if isinstance(item[key], decimal.Decimal):
                item[key] = float(item[key])
    return res_list


def data_format(bean):
    """
    Transfer from datetime.datetime  to [2018:12:12 10:10:56]
    :param bean: dict
    :return:
    """
    if not bean or not isinstance(bean, dict):
        return bean
    for key in bean.keys():
        if isinstance(bean[key], datetime.datetime) \
                or isinstance(bean[key], datetime.date):
            bean[key] = str(bean[key])
        if isinstance(bean[key], decimal.Decimal):
            bean[key] = float(bean[key])
    return bean


if __name__ == '__main__':
    sqlite_client = SqliteClient()
    sqlite_client.init_db()
    proxy = {'ip': '192.168.1.1', 'port': 80, 'protocol': 0,
             'country': '中国', 'area': '广州', 'speed': 11.123, 'types': 0}
    re_in = sqlite_client.insert(proxy)
    print("新增情况", re_in)
    re_up = sqlite_client.update({'ip': '192.168.1.1', 'port': 80}, {'score': 12})
    print("是否修改成功", re_up)
    # returned a tuple
    data = sqlite_client.select(3)
    print("query data: ", data, " data type: ", type(data))
    # sqlite_client.drop_db()
    sqlite_client.close_db()
