# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: cateye.py

@time: 2018/6/17 13:21

@desc:
'''

import re
import requests
import json
import time
from requests.exceptions import RequestException

def get_one_page(offset):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    }
    url = "http://maoyan.com/board/4?offset="+str(offset)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None


def get_one_page_data(content):
    # print(content)
     pattern = re.compile('<dd.*?board-index.*?>(.*?)</i>.*?<a.*?data-src="(.*?)".*?</a>.*?<p.*?<a.*?>(.*?)</a>.*?<p.*?class="star".*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?score.*?integer".*?>(.*?)</i>.*?fraction".*?>(.*?)</i>.*?</dd>',re.S)
     items = re.findall(pattern,content)
     #print(items)
     for item in items:
         yield {
            'index':item[0],
            'image':item[1],
            'title':item[2].strip(),
            'actor':item[3].strip()[3:] if len(item[3])>3 else '',
            'time':item[4].strip()[5:] if len(item[4])>5 else '',
            'score':item[5]+item[6]
         }

def write_to_json(data):
     with open('./top100.txt','a',encoding="utf-8") as file:
         file.write(json.dumps(data,ensure_ascii=False,indent=2))


def get_topN_data(page):
    for i in range(page):
        html = get_one_page(i*10)
        for info in get_one_page_data(html):
            write_to_json(info)
        time.sleep(1)

if __name__=='__main__':
    get_topN_data(10)
