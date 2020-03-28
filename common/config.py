# coding:utf-8

import os
import random

BANNER = """
    ____      ____                        ____              __
   /  _/___  / __ \_________  _  ____  __/ __ \____  ____  / /
   / // __ \/ /_/ / ___/ __ \| |/_/ / / / /_/ / __ \/ __ \/ / 
 _/ // /_/ / ____/ /  / /_/ />  </ /_/ / ____/ /_/ / /_/ / /  
/___/ .___/_/   /_/   \____/_/|_|\__, /_/    \____/\____/_/   
   /_/                          /____/                       

http://www.network-science.de/ascii/
"""

"""
定义规则 urls: url列表
         type：解析方式,取值 regular(正则表达式),xpath(xpath解析),module(自定义第三方模块解析)
         patten：可以是正则表达式,可以是xpath语句不过要和上面的相对应
         属性：ip，port，types(0高匿名，1透明)，protocol(0 http,1 https),country(国家),area(省市),speed(连接速度)
"""
# List of free agents
parser_list = [{
    # http://www.66ip.cn
    'urls': ['http://www.66ip.cn/%s.html' % n for n in ['index'] + list(range(2, 12))],
    'type': 'xpath',
    'pattern': ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': './td[4]', 'protocol': ''}
}, {
    # http://www.66ip.cn
    'urls': ['http://www.66ip.cn/areaindex_%s/%s.html' % (m, n) for m in range(1, 35) for n in range(1, 10)],
    'type': 'xpath',
    'pattern': ".//*[@id='footer']/div/table/tr[position()>1]",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': './td[4]', 'protocol': ''}
}, {
    # http://cn-proxy.com
    'urls': ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218'],
    'type': 'xpath',
    'pattern': ".//table[@class='sortable']/tbody/tr",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': '', 'protocol': ''}
}, {
    # http://www.mimiip.com
    'urls': ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 30)],
    'type': 'xpath',
    'pattern': ".//table[@class='list']/tr",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': '', 'protocol': ''}
}, {
    # https://proxy-list.org
    'urls': ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)],
    'type': 'module',
    'moduleName': 'proxy_list_parser',
    'pattern': 'Proxy\\(.+\\)',
    'position': {'ip': 0, 'port': -1, 'types': -1, 'protocol': 2}
}, {
    # http://incloak.com
    'urls': ['http://incloak.com/proxy-list/%s#list' % n for n in
             ([''] + ['?start=%s' % (64 * m) for m in range(1, 30)])],
    'type': 'xpath',
    'pattern': ".//table[@class='proxy__t']/tbody/tr",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': '', 'protocol': ''}
}, {
    # http://www.kuaidaili.com
    'urls': ['http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 31)],
    'type': 'xpath',
    'pattern': ".//*[@id='index_free_list']/table/tbody/tr[position()>0]",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': './td[3]', 'protocol': './td[4]'}
}, {
    # http://www.kuaidaili.com
    'urls': ['http://www.kuaidaili.com/free/%s/%s/' % (m, n) for m in ['inha', 'intr', 'outha', 'outtr'] for n in
             range(1, 11)],
    'type': 'xpath',
    'pattern': ".//*[@id='list']/table/tbody/tr[position()>0]",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': './td[3]', 'protocol': './td[4]'}
}, {
    # http://www.cz88.net
    'urls': ['http://www.cz88.net/proxy/%s' % m for m in
             ['index.shtml'] + ['http_%s.shtml' % n for n in range(2, 31)]],
    'type': 'xpath',
    'pattern': ".//*[@id='boxright']/div/ul/li[position()>1]",
    'position': {'ip': './div[1]', 'port': './div[2]', 'types': './div[3]', 'protocol': ''}
}, {
    # http://www.ip181.com
    'urls': ['http://www.ip181.com/daili/%s.html' % n for n in range(1, 31)],
    'type': 'xpath',
    'pattern': ".//div[@class='row']/div[3]/table/tbody/tr[position()>1]",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': './td[3]', 'protocol': './td[4]'}
}, {
    # http://www.xicidaili.com
    'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 700)],
    'type': 'xpath',
    'pattern': ".//*[@id='ip_list']/tbody/tr[position()>1]",
    'position': {'ip': './td[2]', 'port': './td[3]', 'types': './td[5]', 'protocol': './td[6]'}
}, {
    # http://www.cnproxy.com
    'urls': ['http://www.cnproxy.com/proxy%s.html' % i for i in range(1, 31)],
    'type': 'module',
    'moduleName': 'cn_proxy_parser',
    'pattern': r'<tr><td>(\d+\.\d+\.\d+\.\d+)<SCRIPT type=text/javascript>document.write\(\"\:\"(.+)\)</SCRIPT></td><td>(HTTP|SOCKS4)\s*',
    'position': {'ip': 0, 'port': 1, 'types': -1, 'protocol': 2}
}, {
    # http://www.ip3366.net(新增)
    'urls': ['http://www.ip3366.net/?stype=%s&page=%s' % (m, n) for m in range(1, 20) for n in range(1, 10)],
    'type': 'xpath',
    'pattern': ".//*[@id='list']/table/tbody/tr[position()>1]",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': './td[3]', 'protocol': './td[4]'}
}, {
    # http://www.qydaili.com/(新增)
    'urls': ['http://www.qydaili.com/free/?action=china&page=%s' % n for n in range(1, 10)],
    'type': 'xpath',
    'pattern': ".//*[@id='content']/section/div[2]/table/tbody/tr[position()>1]",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': './td[3]', 'protocol': './td[4]'}
}, {
    # http://www.89ip.cn/(新增)
    'urls': ['http://www.89ip.cn/index_%s.html' % n for n in range(1, 30)],
    'type': 'xpath',
    'pattern': "./html/body/meta'utf-8'/div[4]/div[1]/div/div[1]/table/tbody/tr[position()>1]",
    'position': {'ip': './td[1]', 'port': './td[2]', 'types': -1, 'protocol': 2}
}]

"""
DataBase Config
Support DB like sqlite;mongodb;redis;mysql
"""
DB_CONFIG = {
    # Sqlite Database
    # 'DB_CONNECT_TYPE': 'sqlite',
    # 'DB_CONNECT_STRING': 'sqlite:///' + os.path.dirname(__file__) + '/data/proxy.db'

    # Mongodb Database
    # 'DB_CONNECT_TYPE': 'mongodb',
    # 'DB_CONNECT_STRING': 'mongodb://localhost:27017/'

    # Redis cache
    # 'DB_CONNECT_TYPE': 'redis',
    # 'DB_CONNECT_STRING': 'redis://:123456@127.0.0.1:6379/8?decode_responses=True'

    # Mysql Database
    'DB_CONNECT_TYPE': 'mysql',
    'DB_CONNECT_STRING': 'mysql+mysqlconnector://root:123456@127.0.0.1/ip_proxy?charset=utf8'
}

"""
China area
"""
CHINA_AREA = [
    '河北', '山东', '辽宁', '黑龙江', '吉林',
    '甘肃', '青海', '河南', '江苏', '湖北',
    '湖南', '江西', '浙江', '广东', '云南',
    '福建', '台湾', '海南', '山西', '四川',
    '陕西', '贵州', '安徽', '重庆', '北京',
    '上海', '天津', '广西', '内蒙', '西藏',
    '新疆', '宁夏', '香港', '澳门']

"""
Pure IP address database qqwry
"""
QQWRY_PATH = os.path.dirname(__file__) + "\\data\\qqwry.dat"

"""
Thread number
"""
THREAD_NUM = 5

"""
Api setting
"""
API_HOST = "127.0.0.1"
API_PORT = 80

"""
爬虫爬取和检测ip的设置条件
不需要检测ip是否已经存在，因为会定时清理
"""
# 每半个小时检测一次是否有代理ip失效
UPDATE_TIME = 30 * 60
# 当有效的ip值小于一个时 需要启动爬虫进行爬取
MIN_NUM = 50
# socket延时
TIMEOUT = 5

"""
反爬虫的设置
"""
# 重试次数
RETRY_TIME = 3
# User-Agent 随机头信息
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def get_header():
    """
    Get header
    :return: header
    """
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        # "Content - Type": "text/html; charset=utf-8"
    }


# 默认给抓取的ip分配20分,每次连接失败,减一分,直到分数全部扣完从数据库中删除
DEFAULT_SCORE = 10
# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://ip.chinaz.com/getip.aspx'
TEST_IP = 'http://httpbin.org/ip'
TEST_HTTP_HEADER = 'http://httpbin.org/get'
TEST_HTTPS_HEADER = 'https://httpbin.org/get'
# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

"""
# CHECK_PROXY变量是为了用户自定义检测代理的函数
# 现在使用检测的网址是httpbin.org,但是即使ip通过了验证和检测
# 也只能说明通过此代理ip可以到达httpbin.org,但是不一定能到达用户爬取的网址
# 因此在这个地方用户可以自己添加检测函数,我以百度为访问网址尝试一下
# 大家可以看一下Validator.py文件中的baidu_check函数和detect_proxy函数就会明白
"""
# 检测代理是否可用
CHECK_PROXY = {'function': 'check_proxy'}

"""
下面配置squid,现在还没实现
SQUID={'path':None,'confpath':'C:/squid/etc/squid.conf'}
"""
# CHECK_PROXY最大进程数
MAX_CHECK_PROCESS = 2
# CHECK_PROXY时每个进程的最大并发
MAX_CHECK_CONCURRENT_PER_PROCESS = 30
# 任务队列SIZE
TASK_QUEUE_SIZE = 50
# 从免费代理网站下载时的最大并发
MAX_DOWNLOAD_CONCURRENT = 3
# 进程数达到上限时的等待时间
CHECK_WAIT_TIME = 1
