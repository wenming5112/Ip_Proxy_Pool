# coding:utf-8
from gevent import monkey

from utils.LogHandler import Logger

monkey.patch_all()
import json
import os
import time

import chardet

import gevent
import psutil
import requests

import common.config as config
from db.DataStore import sql_helper
from exception.BaseException import TestUrlFail

from multiprocessing import Process, Queue

log = Logger.log_handler


def detect_from_db(proxy, proxies_set):
    if isinstance(proxy, dict):
        log.debug("ip : %s -- port : %s" % (proxy.get("ip"), proxy.get("port")))
        # proxy_dict = {'ip': proxy[0], 'port': proxy[1]}
        result = detect_proxy(proxy)
        if result:
            proxy_str = "%s:%s" % (proxy.get("ip"), proxy.get("port"))
            proxies_set.add(proxy_str)
        else:
            if proxy.get("score") < 1:
                sql_helper.delete({"ip": proxy.get("ip"), "port": proxy.get("port")})
            else:
                score = proxy.get("score") - 1
                sql_helper.update({"ip": proxy.get("ip"), "port": proxy.get("port")}, {"score": score})
                proxy_str = "%s:%s" % (proxy.get("ip"), proxy.get("port"))
                proxies_set.add(proxy_str)
    else:
        raise Exception("Invalid data type, need dict, but got %s" % type(proxy))


def validator(queue1, queue2):
    task_list = []
    # 所有进程列表
    proc_pool = {}
    # 控制信息队列
    control_q = Queue()
    pid = None
    while True:
        if not control_q.empty():
            # 处理已结束的进程
            try:
                pid = control_q.get()
                proc_pool.pop(pid)
                proc_ps = psutil.Process(pid)
                proc_ps.kill()
                proc_ps.wait()
            except Exception as e:
                log.warning(e.__str__())
                log.warning("we are unable to kill pid:%s" % pid)
                pass
        try:
            # proxy_dict = {'source':'crawl','data':proxy}
            if len(proc_pool) >= config.MAX_CHECK_PROCESS:
                time.sleep(config.CHECK_WAIT_TIME)
                continue
            proxy = queue1.get()
            task_list.append(proxy)
            if len(task_list) >= config.MAX_CHECK_CONCURRENT_PER_PROCESS:
                p = Process(target=process_start, args=(task_list, queue2, control_q))
                p.start()
                proc_pool[p.pid] = p
                task_list = []
        except Exception as e:
            log.warning(e.__str__())
            if len(task_list) > 0:
                p = Process(target=process_start, args=(task_list, queue2, control_q))
                p.start()
                proc_pool[p.pid] = p
                task_list = []


def process_start(tasks, queue2, control_queue):
    """
    Start process
    :param tasks: proxy
    :param queue2: queue
    :param control_queue: control queue
    """
    spawns = []
    for task in tasks:
        spawns.append(gevent.spawn(detect_proxy, task, queue2))
    gevent.joinall(spawns)
    # Join the control queue when the child process exits
    control_queue.put(os.getpid())


def detect_proxy(proxy, queue2=None):
    """
    Detects whether the agent is available
    :param proxy: proxy dict include ip and port
    :param queue2: a queue default None
    :return: None or proxy dict
    """
    ip = proxy['ip']
    port = proxy['port']
    protocol, speed, types = __check_proxy_a(__get_format_proxy(ip, port))
    if protocol >= 0:
        proxy['protocol'] = protocol
        proxy['types'] = types
        proxy['speed'] = speed
    else:
        proxy = None
    if queue2:
        queue2.put(proxy)
    return proxy


def __check_proxy_a(proxy):
    """
    Detects whether the agent is available
    :param proxy: proxy str
    :return: tuple(protocol, speed, types)
    """
    try:
        start = time.time()
        r = requests.get(url=config.TEST_URL, headers=config.get_header(),
                         timeout=config.TIMEOUT, proxies=proxy)
        r.encoding = chardet.detect(r.content)['encoding']
        if r.ok:
            speed = round(time.time() - start, 2)
            protocol = 0
            types = 0
            return protocol, speed, types
        else:
            return __check_proxy_b(proxy)
    except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
            requests.exceptions.ChunkedEncodingError):
        return __check_proxy_b(proxy)


def __check_proxy_b(proxies):
    """
     Another way to detect whether the agent is available
    :param proxies: proxy dict like {"http": "http://218.60.8.99:3129", "https": "http://218.60.8.99:3129" }
    :return: tuple(protocol, speed, types)
    """
    http, http_types, http_speed = __check_http_proxy(proxies)
    https, https_types, https_speed = __check_http_proxy(proxies, False)
    if http and https:
        protocol = 2
        types = http_types
        speed = http_speed
    elif http:
        types = http_types
        protocol = 0
        speed = http_speed
    elif https:
        types = https_types
        protocol = 1
        speed = https_speed
    else:
        types = -1
        protocol = -1
        speed = -1
    return protocol, speed, types


def __check_http_proxy(proxies, is_http=True):
    types = -1
    speed = -1
    if is_http:
        test_url = config.TEST_HTTP_HEADER
    else:
        test_url = config.TEST_HTTPS_HEADER
    try:
        start = time.time()
        r = requests.get(url=test_url, headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
        if r.ok:
            speed = round(time.time() - start, 2)
            content = json.loads(r.text)
            headers = content['headers']
            ip = content['origin']
            proxy_connection = headers.get('Proxy-Connection', None)
            if ',' in ip:
                types = 2
            elif proxy_connection:
                types = 1
            else:
                types = 0
            return True, types, speed
        else:
            return False, types, speed
    except Exception as e:
        log.warning(e.args)
        return False, types, speed


def get_target_ip():
    """
    Crawl what website to get its IP, this is not a proxy IP
    :return:
    """
    try:
        r = requests.get(url=config.TEST_IP, headers=config.get_header(), timeout=config.TIMEOUT)
        ip = json.loads(r.text)
        return ip['origin']
    except Exception:
        raise TestUrlFail


def __get_format_proxy(ip, port):
    return {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}


if __name__ == '__main__':
    ip_t = "101.132.39.115"
    port_t = 8080
    # proxy_t = __get_format_proxy(ip_t, port_t)
    # print("target --> ", get_target_ip())
    # a = __check_proxy_b(proxy_t)
    # print("a的类型 --> ", type(a))
    # print("a的全部结果 --> ", a)
    # print(a[0])

    proxy_dict_t = {"ip": ip_t, "port": port_t}
    my_re = detect_proxy(proxy_dict_t)
    print(my_re)
    if my_re is None:
        print("这个代理不可用")
    else:
        print("返回结果", my_re)
        print("代理可用")
