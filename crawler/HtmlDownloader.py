# coding:utf-8

import random

import common.config as config
from db.DataStore import sql_helper

__author__ = 'qiye'

import requests
import chardet


class HtmlDownloader(object):
    @staticmethod
    def download(url):
        try:
            r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT)
            r.encoding = chardet.detect(r.content)['encoding']
            if (not r.ok) or len(r.content) < 500:
                raise ConnectionError
            else:
                return r.text

        except Exception as e:
            print(e.args)
            count = 0  # 重试次数
            proxy_list = sql_helper.select(10)
            if not proxy_list:
                return None

            while count < config.RETRY_TIME:
                try:
                    proxy = random.choice(proxy_list)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}

                    r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
                    r.encoding = chardet.detect(r.content)['encoding']
                    if (not r.ok) or len(r.content) < 500:
                        raise ConnectionError
                    else:
                        return r.text
                except Exception:
                    count += 1

        return None
