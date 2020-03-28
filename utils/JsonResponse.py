# coding: utf-8
"""
------------------------------------------------------------
   File Name: JsonResponse.py
   Description: Uniform format response
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: Uniform format response
------------------------------------------------------------
"""
import json

__author__ = 'JockMing'


class HttpCode(object):
    """
    Custom status code
    """
    # Normal response status code
    success_code = 200
    # Parameter error
    params_error_code = 400
    # Permissions error
    un_auth = 401
    # Method error
    method_error = 405
    # Server internal error
    server_error = 500


class JsonResponse(object):
    # Define a uniform json string return format
    @classmethod
    def _result(cls, code=HttpCode.success_code, msg="", data=None, kwargs=None):
        json_dict = {"code": code, "msg": msg, "data": data}
        if kwargs and isinstance(kwargs, dict) and kwargs.keys():
            json_dict.update(kwargs)
        return json.dumps(json_dict, ensure_ascii=False, indent=3)

    @classmethod
    def success(cls, msg="", data=None):
        """
        Normal response
        :param msg: Message
        :param data: Default None
        :return: HttpResponse: Json
        """
        return cls._result(msg=msg, data=data)

    @classmethod
    def params_error(cls, msg="", data=None):
        """
        Parameter error
        :param msg: Message
        :param data: Default None
        :return: HttpResponse: Json
        """
        return cls._result(code=HttpCode.params_error_code, msg=msg, data=data)

    @classmethod
    def un_auth(cls, msg="", data=None):
        """
        Permission error
        :param msg: Message
        :param data: Default None
        :return: HttpResponse: Json
        """
        return cls._result(code=HttpCode.un_auth, msg=msg, data=data)

    @classmethod
    def method_error(cls, msg="", data=None):
        """
        Method error
        :param msg: Message
        :param data: Default None
        :return: HttpResponse: Json
        """
        return cls._result(code=HttpCode.method_error, msg=msg, data=data)

    @classmethod
    def server_error(cls, msg="", data=None):
        """
        Server internal error
        :param msg: Message
        :param data: Default None
        :return: HttpResponse: Json
        """
        return cls._result(code=HttpCode.server_error, msg=msg, data=data)
