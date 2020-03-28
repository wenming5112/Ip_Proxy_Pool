import random
import re

import requests
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError

from common.config import TEST_URL
from common.config import USER_AGENTS
from common.config import get_header


def get_page(url, options=None):
    """
    Crawl the proxy
    :param url: Url
    :param options: opt
    :return:
    """
    if options is None:
        options = {}
    print('Crawling', url)
    headers = dict(get_header(), **options)
    print("Print headers:", headers)
    try:
        response = requests.get(url, timeout=5, headers=headers)
        print("Crawl success", url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('Crawl failed', url)
        return None


def check_ip(proxy_str):
    print("Checking ip:  %s" % proxy_str)
    proxy = {
        "http": proxy_str,
        "https": proxy_str
    }
    try:
        status_code = requests.get(TEST_URL, timeout=5, proxies=proxy).status_code
        print("Usable Proxy IP: {}".format(proxy_str))
        if status_code == 200:
            return True
        else:
            return False
    except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
            requests.exceptions.ChunkedEncodingError):
        print("Unusable Proxy IP: {}".format(proxy_str))
        return False


def crawler_01():
    """
    http://www.ip3366.net
    :return: ip:port
    """
    for i in range(1, 10):
        start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>(\\d+\\.\\d+\\.\\d+\\.\\d+)</td>')
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>(\\d+)</td>')
                re_port = find_port.findall(trs[s])
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ":" + port
                    # This is equivalent to a return statement
                    yield address_port.replace(' ', '')


def crawler_02():
    """
    http://www.kuaidaili.com
    :return: ip:port
    """
    for i in range(1, 3000):
        start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
        html = get_page(start_url)
        if html:
            ip_address = re.compile('<td data-title="IP">(.*?)</td>')
            re_ip_address = ip_address.findall(html)
            port = re.compile('<td data-title="PORT">(.*?)</td>')
            re_port = port.findall(html)
            for address, port in zip(re_ip_address, re_port):
                address_port = address + ':' + port
                yield address_port.replace(' ', '')


def crawler_03():
    """
    http://www.xicidaili.com
    :return: ip:port
    """
    for i in range(1, 4000):
        start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
            'Host': 'www.xicidaili.com',
            'Referer': 'http://www.xicidaili.com/nn/3',
            'Upgrade-Insecure-Requests': '1'
        }
        html = get_page(start_url, options=headers)
        if html:
            find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
            trs = find_trs.findall(html)
            for tr in trs:
                find_ip = re.compile('<td>(\\d+\\.\\d+\\.\\d+\\.\\d+)</td>')
                re_ip_address = find_ip.findall(tr)
                find_port = re.compile('<td>(\\d+)</td>')
                re_port = find_port.findall(tr)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')


def crawler_04(page_count=1900):
    """
    http://www.66ip.cn
    :param page_count: 页码
    :return: 代理
    """
    start_url = 'http://www.66ip.cn/{}.html'
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    for url in urls:
        print('Crawling', url)
        html = get_page(url)
        if html:
            doc = pq(html)
            trs = doc('.containerbox table tr:gt(0)').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1)').text()
                port = tr.find('td:nth-child(2)').text()
                yield ':'.join([ip, port])


if __name__ == '__main__':

    # r1 = crawler_01()
    # for it in r1:
    #     check_ip(it)
    # 存放可用的IP代理
    list_x = []
    r2 = crawler_03()
    for it in r2:
        a = check_ip(it)
        if a:
            list_x.append(it)
