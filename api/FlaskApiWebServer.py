"""
------------------------------------------------------------
   File Name: TestFlaskWebServer.py
   Description: Flask framework test
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
    Change Activity:
    2020/03/21 -- Flask framework test


------------------------------------------------------------
    Note:
    The application is the xxx.py like current file for your service
    and should be at the same level as templates
------------------------------------------------------------
"""
import platform

__author__ = 'JockMing'

from flask import Flask, jsonify, request
from werkzeug.wrappers import Response

from common.config import *
from db.DataStore import sql_helper
from utils.JsonResponse import JsonResponse
from utils.LogHandler import Logger

__all__ = ['app']

app = Flask(__name__)
log = Logger.log_handler


class JsonResult(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResult, cls).force_type(response, environ)


app.response_class = JsonResult

api_list = {
    "search": u"Select all useful proxy",
    "search?count=10": u"Get a certain number of proxy",
    "delete?": u'delete an unable proxy'
}


@app.route('/')
def index():
    return api_list


@app.route("/search", methods=["GET"])
def search():
    inputs = request.args
    log.info(inputs)
    data = sql_helper.select(inputs.get('count', None), inputs)
    return JsonResponse.success("查询成功", data)


@app.route("/delete", methods=["GET"])
def delete():
    inputs = request.args
    print(inputs)
    data = sql_helper.delete(inputs)
    return JsonResponse.success("操作成功", data)


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT)
