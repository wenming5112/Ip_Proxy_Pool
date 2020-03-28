# coding:utf-8
"""
------------------------------------------------------------
   File Name: Proxy.py
   Description: Proxy entity class
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Proxy entity class
------------------------------------------------------------
"""
import datetime

from sqlalchemy import Column, Integer, DateTime, Numeric, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

from common.config import DEFAULT_SCORE

BaseModel = declarative_base()


class Proxy(BaseModel):
    __tablename__ = "proxy"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    types = Column(Integer, nullable=False)
    protocol = Column(Integer, nullable=False, default=0)
    country = Column(VARCHAR(100), nullable=False)
    area = Column(VARCHAR(100), nullable=False)
    update_time = Column(DateTime(), default=datetime.datetime.utcnow)
    speed = Column(Numeric(5, 2), nullable=False)
    score = Column(Integer, nullable=False, default=DEFAULT_SCORE)
