FROM python:3.7

MAINTAINER JockMing <an23gn@163.com>

ENV TZ Asia/Shanghai

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY . .

EXPOSE 80

WORKDIR /usr/src/app

ENTRYPOINT [ "sh", "start.sh" ]
