# coding:utf-8
import sys
import time

from gevent import monkey

from common.config import THREAD_NUM, parser_list, UPDATE_TIME, MIN_NUM, MAX_CHECK_CONCURRENT_PER_PROCESS, \
    MAX_DOWNLOAD_CONCURRENT
from db.DataStore import sql_helper
from validator.Validator import detect_from_db

monkey.patch_all()
from multiprocessing import Queue, Value

import gevent

from gevent.pool import Pool

from crawler.HtmlDownloader import HtmlDownloader
from crawler.HtmlPraser import HtmlParser

__author__ = 'qiye'


def start_proxy_crawl(queue, db_proxy_num):
    crawl = ProxyCrawl(queue, db_proxy_num)
    crawl.run()


class ProxyCrawl(object):
    proxies = set()

    def __init__(self, queue, db_proxy_num):
        self.crawl_pool = Pool(THREAD_NUM)
        self.queue = queue
        self.db_proxy_num = db_proxy_num

    def run(self):
        while True:
            self.proxies.clear()
            str_x = 'Ip_Proxy_Pool ------>>>>>> beginning'
            sys.stdout.write(str_x + "\r\n")
            sys.stdout.flush()
            proxy_list = sql_helper.select()

            spawns = []
            for proxy in proxy_list:
                spawns.append(gevent.spawn(detect_from_db, proxy, self.proxies))
                if len(spawns) >= MAX_CHECK_CONCURRENT_PER_PROCESS:
                    gevent.joinall(spawns)
                    spawns = []
            gevent.joinall(spawns)
            self.db_proxy_num.value = len(self.proxies)
            str_x = 'IPProxyPool----->>>>>>>>db exists ip:%d' % len(self.proxies)
            if len(self.proxies) < MIN_NUM:
                str_x += '\r\nIPProxyPool----->>>>>>>>now ip num < MINNUM,start crawling...'
                sys.stdout.write(str_x + "\r\n")
                sys.stdout.flush()
                spawns = []
                for p in parser_list:
                    spawns.append(gevent.spawn(self.crawl, p))
                    if len(spawns) >= MAX_DOWNLOAD_CONCURRENT:
                        gevent.joinall(spawns)
                        spawns = []
                gevent.joinall(spawns)
            else:
                str_x += '\r\nIPProxyPool----->>>>>>>>now ip num meet the requirement,wait UPDATE_TIME...'
                sys.stdout.write(str_x + "\r\n")
                sys.stdout.flush()

            time.sleep(UPDATE_TIME)

    def crawl(self, parser):
        html_parser = HtmlParser()
        for url in parser['urls']:
            response = HtmlDownloader.download(url)
            if response is not None:
                proxy_list = html_parser.parser_exec(response, parser)
                if proxy_list is not None:
                    for proxy in proxy_list:
                        proxy_str = '%s:%s' % (proxy['ip'], proxy['port'])
                        if proxy_str not in self.proxies:
                            self.proxies.add(proxy_str)
                            while True:
                                if self.queue.full():
                                    time.sleep(0.1)
                                else:
                                    self.queue.put(proxy)
                                    break


if __name__ == "__main__":
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue()
    spider = ProxyCrawl(q1, DB_PROXY_NUM)
    spider.run()
