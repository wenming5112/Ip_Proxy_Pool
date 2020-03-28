"""
------------------------------------------------------------
   File Name: TestFlaskWebServer.py
   Description: Flask framework test
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
    Change Activity:
    2020/03/21 -- Flask framework test


------------------------------------------------------------
    Note:
    The application is the xxx.py like current file for your service
    and should be at the same level as templates
------------------------------------------------------------
"""
__author__ = 'JockMing'
from flask import Flask, render_template, request

from common.config import *
from flask_bootstrap import Bootstrap

__all__ = ['app']

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    # arguments
    condition = request.args.get('q')
    return 'The query parameters submitted by the user are: {}'.format(condition)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':

        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        print('username: {}, password: {}'.format(username, password))
        return 'name = {}, password = {}'.format(username, password)


if __name__ == '__main__':
    app.run(debug=True, host=API_HOST, port=API_PORT)
