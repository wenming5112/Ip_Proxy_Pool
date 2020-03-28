# coding:utf-8
import base64
import re

from common.config import QQWRY_PATH, CHINA_AREA
from utils.IPAddress import IpAddress
from utils.LogHandler import Logger
from utils.compatibility import text_

__author__ = 'qiye'

from lxml import html

log = Logger.log_handler


class HtmlParser(object):
    def __init__(self):
        self.ips = IpAddress(QQWRY_PATH)

    def parser_exec(self, response, parser):
        """
        Parser
        :param response: xxx
        :param parser: xxx
        :return:
        """
        if parser['type'] == 'xpath':
            return self.__xpath_parser(response, parser)
        elif parser['type'] == 'regular':
            return self.__regular_parser(response, parser)
        elif parser['type'] == 'module':
            return getattr(self, parser['moduleName'], None)(response, parser)
        else:
            return None

    @classmethod
    def home_country(cls, addr):
        """
        To determine which country the address is from
        :param addr:
        :return:
        """
        for area in CHINA_AREA:
            if text_(area) in addr:
                return True
        return False

    def __xpath_parser(self, response, parser):
        """
        Parsing against xpath methods
        :param response:
        :param parser:
        :return:
        """
        proxy_list = []
        root = html.etree.HTML(response)
        proxies = root.xpath(parser['pattern'])
        for proxy in proxies:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = proxy.xpath(parser['position']['port'])[0].text
                types = 0
                protocol = 0
                addr = self.ips.getIpAddr(self.ips.str_to_ip(ip))
                if text_('省') in addr or self.home_country(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr
            except Exception as e:
                print(e.__str__())

                continue
            # ip，port，types(0高匿名，1透明)，protocol(0 http,1 https http),country,area,speed
            proxy = {'ip': ip, 'port': int(port), 'types': int(types), 'protocol': int(protocol),
                     'country': country, 'area': area, 'speed': 100}
            proxy_list.append(proxy)
        return proxy_list

    def __regular_parser(self, response, parser):
        """
        Parsing for regular expressions
        :param response:
        :param parser:
        :return:
        """
        proxy_list = []
        pattern = re.compile(parser['pattern'])
        matches = pattern.findall(response)
        if matches is not None:
            for match in matches:
                try:
                    ip = match[parser['position']['ip']]
                    port = match[parser['position']['port']]
                    # The type of the site has not been reliable so it is still the default, will be detected later
                    types = 0
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str_to_ip(ip))
                    # print(ip,port)
                    if text_('省') in addr or self.home_country(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    log.warning(e.args)
                    continue
                proxy = {'ip': ip, 'port': port, 'types': types, 'protocol': protocol, 'country': country, 'area': area,
                         'speed': 100}

                proxy_list.append(proxy)
            return proxy_list

    def cn_proxy_parser(self, response, parser):
        proxy_list = self.__regular_parser(response, parser)
        char_dict = {'v': '3', 'm': '4', 'a': '2', 'l': '9', 'q': '0', 'b': '5', 'i': '7', 'w': '6', 'r': '8', 'c': '1'}

        for proxy in proxy_list:
            port = proxy['port']
            new_port = ''
            for i in range(len(port)):
                if port[i] != '+':
                    new_port += char_dict[port[i]]
            new_port = int(new_port)
            proxy['port'] = new_port
        return proxy_list

    def proxy_list_parser(self, response, parser):
        proxy_list = []
        pattern = re.compile(parser['pattern'])
        matches = pattern.findall(response)
        if matches:
            for match in matches:
                try:
                    ip_port = base64.b64decode(match.replace("Proxy('", "").replace("')", ""))
                    ip = ip_port.split(':')[0]
                    port = ip_port.split(':')[1]
                    types = 0
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str_to_ip(ip))
                    # print(ip,port)
                    if text_('省') in addr or self.home_country(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    log.warning(e.args)
                    continue
                proxy = {'ip': ip, 'port': int(port), 'types': types, 'protocol': protocol, 'country': country,
                         'area': area, 'speed': 100}
                proxy_list.append(proxy)
            return proxy_list
