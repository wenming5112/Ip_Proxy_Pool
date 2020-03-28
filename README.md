# Ip_Proxy_Pool

![](https://img.shields.io/badge/Ip_Proxy_Pool-dev-brightgreen.svg)
![build](https://github.com/Python3WebSpider/ProxyPool/workflows/build/badge.svg)
![deploy](https://github.com/Python3WebSpider/ProxyPool/workflows/deploy/badge.svg)
![](https://img.shields.io/badge/python-3.7%2B-brightgreen)
[![](https://img.shields.io/badge/cnblogs-@jockming-blue.svg)](https://www.cnblogs.com/jockming/)
![](https://img.shields.io/badge/platform-Windows|Linux-lightgrey.svg)

**Reference code:** [@JHao104](http://www.spiderpy.cn/blog/)

**Reference code:** [@qiye](http://www.cnblogs.com/qiyeboy/p/5693128.html)

```
    ____      ____                        ____              __
   /  _/___  / __ \_________  _  ____  __/ __ \____  ____  / /
   / // __ \/ /_/ / ___/ __ \| |/_/ / / / /_/ / __ \/ __ \/ / 
 _/ // /_/ / ____/ /  / /_/ />  </ /_/ / ____/ /_/ / /_/ / /  
/___/ .___/_/   /_/   \____/_/|_|\__, /_/    \____/\____/_/   
   /_/                          /____/                       

http://www.network-science.de/ascii/
```


## Overview

> _Just for learning_

> _This project continuously crawls the free proxy IP published on the proxy website through crawler, verifies and maintains the proxy that can be used in real time, and provides external use in the form of API._


- api_start
- start_proxy_crawl
- validator
- store_data


- [x] web api
- [x] Proxy periodic inspection
- [x] Support mysql db
- [ ] Support redis
- [x] Support sqlite
- [x] Support MongoDB
- [ ] Support SSDB


## Pre-requisites
The following tools are required to run this project:
- Git
- Python-3.7
- Need to install one of MySQL / Redis / MongoDB databases

## How to start?

### 



### Running projects from source on Windows
```shell
# clone the source code
git clone ***

cd Ip_Proxy_Pool

pip install -r requirements.txt
```

### Running projects from source on Linux
```shell
# clone the source code
git clone ***

cd Ip_Proxy_Pool

pip install -r requirements.txt
```

### Using the Docker image
```bash
docker run -it -d ***
```

### Using docker-compose
The above command is more readable when converted to a docker-compose.yaml file:
```yaml
version: '2'

services:
    caliper:
        container_name: ip_proxy
        image: proxy
        command: proxy run
        environment:
          - DB_TYPE=redis
          - DB_PORT=6379
          - DB_PASSWORD=123456
        volumes:
          - xxx/xxx:rw
        ports:
          - 80:80
```