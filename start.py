# coding:utf-8
from multiprocessing import Queue, Value, Process

import click

from api.FlaskApiWebServer import app
from common.config import TASK_QUEUE_SIZE, API_HOST, API_PORT, BANNER
from crawler.ProxyCrawler import start_proxy_crawl
from db.DataStore import store_data
from validator.Validator import validator

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="1.0.0")
def proxy_server():
    """Ip_Proxy_Pool Server"""


def api_start():
    app.run(host=API_HOST, port=API_PORT)


@proxy_server.command(name="up")
def runner():
    """ Run ip proxy crawler """
    click.echo(BANNER)
    db_proxy_num = Value('i', 0)
    q1 = Queue(maxsize=TASK_QUEUE_SIZE)
    q2 = Queue()
    p0 = Process(target=api_start)
    p1 = Process(target=start_proxy_crawl, args=(q1, db_proxy_num))
    p2 = Process(target=validator, args=(q1, q2))
    p3 = Process(target=store_data, args=(q2, db_proxy_num))

    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p0.join()
    p1.join()
    p2.join()
    p3.join()


if __name__ == '__main__':
    proxy_server()
