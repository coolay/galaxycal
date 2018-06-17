# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: flaskt.py

@time: 2018/6/2 9:14

@desc:
'''

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return 'hello world'
if __name__=='__main__':
    app.run()

