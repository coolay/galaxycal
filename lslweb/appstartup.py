# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: appstartup.py

@time: 2018/5/25 21:03

@desc:
'''
from aiohttp import web
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)

def index(request):
    web.Response(body=b'<h1>Welcome!<h1>',content_type="text/html")

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET','/',index)
    srv = yield  from loop.create_server(app.make_handler(),host='127.0.0.1',port=9000)
    logging.info("server started at http://127.0.0.1:9000...")
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()


