import os

from utils.IPAddress import IpAddress

if __name__ == '__main__':
    QQWRY_PATH = os.path.dirname(__file__) + "/../common/data/qqwry.dat"
    ips = IpAddress(QQWRY_PATH)
    addr_x = ips.getIpAddr(ips.str_to_ip('183.61.236.53'))
    print(addr_x)
