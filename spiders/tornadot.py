
# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: tornadot.py

@time: 2018/6/2 9:22

@desc:
'''

import  tornado.ioloop
import tornado.web

class MainHandle(tornado.web.RequestHandler):
    def get(self):
        self.write("hello,tornado")

class MainHandle_1(tornado.web.RequestHandler):
    def get(self):
        self.write("hello,mic")

def make_app():
    return tornado.web.Application([(r'/',MainHandle),(r'/mic',MainHandle_1)])
if  __name__ == '__main__':
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()