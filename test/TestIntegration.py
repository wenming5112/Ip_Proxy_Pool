# coding:utf-8
from multiprocessing import Queue, Value, Process

from api.FlaskApiWebServer import app
from common.config import TASK_QUEUE_SIZE, API_HOST, API_PORT
from crawler.ProxyCrawler import start_proxy_crawl
from db.DataStore import store_data
from validator.Validator import validator


def api_start():
    app.run(host=API_HOST, port=API_PORT)


if __name__ == '__main__':
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue(maxsize=TASK_QUEUE_SIZE)
    q2 = Queue()
    p0 = Process(target=api_start)
    p1 = Process(target=start_proxy_crawl, args=(q1, DB_PROXY_NUM))
    p2 = Process(target=validator, args=(q1, q2))
    p3 = Process(target=store_data, args=(q2, DB_PROXY_NUM))

    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p0.join()
    p1.join()
    p2.join()
    p3.join()
