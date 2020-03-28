# coding: utf-8
"""
------------------------------------------------------------
   File Name: InterfaceDb.py
   Description: Database operation client interface
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Database operation client interface
------------------------------------------------------------
"""
__author__ = 'JockMing'


class InterfaceDb(object):
    """
    Interface of db
    """
    params = {"ip": None, "port": None, "types": None, "protocol": None, "country": None, "area": None}

    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def close_db(self):
        raise NotImplemented

    def insert(self, value=None):
        raise NotImplemented

    def delete(self, conditions=None):
        raise NotImplemented

    def update(self, conditions=None, value=None):
        raise NotImplemented

    def select(self, count=None, conditions=None):
        raise NotImplemented
