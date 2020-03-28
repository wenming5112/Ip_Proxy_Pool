#! /usr/bin/env python
# coding:utf-8
import os
import socket
import struct

from utils.LogHandler import Logger

log = Logger.log_handler
__author__ = 'qiye'


class IpAddress:
    def __init__(self, ip_db_file):
        self.ip_db = open(ip_db_file, "rb")
        str_x = self.ip_db.read(8)
        (self.first_index, self.last_index) = struct.unpack('II', str_x)
        self.index_count = int((self.last_index - self.first_index) / 7 + 1)
        # print self.getVersion(), u" 纪录总数: %d 条 "%(self.indexCount)

    def get_version(self):
        s = self.getIpAddr(0xffffff00)
        return s

    def get_area_addr(self, offset=0):
        if offset:
            self.ip_db.seek(offset)
        str_x = self.ip_db.read(1)
        (byte,) = struct.unpack('B', str_x)
        if byte == 0x01 or byte == 0x02:
            p = self.get_long_3()
            if p:
                return self.get_string(p)
            else:
                return ""
        else:
            self.ip_db.seek(-1, 1)
            return self.get_string(offset)

    def get_addr(self, offset):
        self.ip_db.seek(offset + 4)
        str_x = self.ip_db.read(1)
        (byte,) = struct.unpack('B', str_x)
        if byte == 0x01:
            country_off_set = self.get_long_3()
            self.ip_db.seek(country_off_set)
            str_x = self.ip_db.read(1)
            (b,) = struct.unpack('B', str_x)
            if b == 0x02:
                country_addr = self.get_string(self.get_long_3())
                self.ip_db.seek(country_off_set + 4)
            else:
                country_addr = self.get_string(country_off_set)
            area_addr = self.get_area_addr()
        elif byte == 0x02:
            country_addr = self.get_string(self.get_long_3())
            area_addr = self.get_area_addr(offset + 8)
        else:
            country_addr = self.get_string(offset + 4)
            area_addr = self.get_area_addr()
        return country_addr + " " + area_addr

    def dump(self, first, last):
        if last > self.index_count:
            last = self.index_count
        for index in range(first, last):
            offset = self.first_index + index * 7
            self.ip_db.seek(offset)
            buf = self.ip_db.read(7)
            (ip, of1, of2) = struct.unpack("IHB", buf)
            address_x = self.get_addr(of1 + (of2 << 16))
            # 把GBK转为utf-8
            # address = str(address_x, 'gbk').encode("utf-8")
            address = str(bytes(address_x, encoding='utf-8'), 'gbk').encode("utf-8")
            log.info("%d %s %s" % (index, self.ip_to_str(ip), address))

    def set_ip_range(self, index):
        offset = self.first_index + index * 7
        self.ip_db.seek(offset)
        buf = self.ip_db.read(7)
        (self.cur_start_ip, of1, of2) = struct.unpack("IHB", buf)
        self.cur_end_ip_offset = of1 + (of2 << 16)
        self.ip_db.seek(self.cur_end_ip_offset)
        buf = self.ip_db.read(4)
        (self.cur_end_ip,) = struct.unpack("I", buf)

    def getIpAddr(self, ip):
        L = 0
        R = self.index_count - 1
        while L < R - 1:
            M = int((L + R) / 2)
            self.set_ip_range(M)
            if ip == self.cur_start_ip:
                L = M
                break
            if ip > self.cur_start_ip:
                L = M
            else:
                R = M
        self.set_ip_range(L)
        # version information, 255.255.255.X, urgy but useful
        if ip & 0xffffff00 == 0xffffff00:
            self.set_ip_range(R)
        if self.cur_start_ip <= ip <= self.cur_end_ip:
            address = self.get_addr(self.cur_end_ip_offset)
            # 把GBK转为utf-8
            address = str(address)
        else:
            address = "未找到该IP的地址"
        return address

    def get_ip_range(self, ip):
        self.getIpAddr(ip)
        range_x = self.ip_to_str(self.cur_start_ip) + ' - ' + self.ip_to_str(self.cur_end_ip)
        return range_x

    def get_string(self, offset=0):
        if offset:
            self.ip_db.seek(offset)
        str_x = b''
        ch = self.ip_db.read(1)
        (byte,) = struct.unpack('B', ch)
        while byte != 0:
            str_x += ch
            ch = self.ip_db.read(1)
            (byte,) = struct.unpack('B', ch)
        return str_x.decode('gbk')

    def ip_to_str(self, ip):
        return str(ip >> 24) + '.' + str((ip >> 16) & 0xff) + '.' + str((ip >> 8) & 0xff) + '.' + str(ip & 0xff)

    def str_to_ip(self, s):
        (ip,) = struct.unpack('I', socket.inet_aton(s))
        return ((ip >> 24) & 0xff) | ((ip & 0xff) << 24) | ((ip >> 8) & 0xff00) | ((ip & 0xff00) << 8)

    def get_long_3(self, offset=0):
        if offset:
            self.ip_db.seek(offset)
        str_x = self.ip_db.read(3)
        (a, b) = struct.unpack('HB', str_x)
        return (b << 16) + a


QQWRY_PATH = os.path.dirname(__file__) + "/../common/data/qqwry.dat"
ips = IpAddress(QQWRY_PATH)
addr_x = ips.getIpAddr(ips.str_to_ip('183.61.236.53'))
print(addr_x)
