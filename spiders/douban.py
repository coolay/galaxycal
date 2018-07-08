# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: douban.py

@time: 2018/6/17 14:52

@desc:
'''

import lxml
from bs4 import BeautifulSoup
import requests
import json
import time
from requests.exceptions import RequestException

def get_one_page(start):
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"

    }
    url = "https://movie.douban.com/top250?start="+str(start)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None


def get_one_page_data(content):
     #print(content)
     soup =  BeautifulSoup(content,"lxml")
     ol = soup.find(class_="grid_view")
     #print(ol)
     liList = ol.find_all(name="li")
     for li in liList:

            yield  {
                    'index':li.find(name='em').string,
                    'detail_url':li.find(class_='pic').find(name="a").attrs['href'],
                    'image':li.find(class_='pic').find(name="img").attrs['src'],
                    'title':(''.join([x.string for x in li.find_all(class_='title')])+li.find(class_='other').string).replace("&nbsp;",""),
                   'time&actor':li.find(class_='bd').select('p')[0].getText().replace("\n","").strip(),
                    'score':li.find(class_='rating_num').string,
                    'assesser':'.'.join([child.string for i,child in enumerate(li.find(class_="star").children) if i==3 ]),
                    'quote':li.find(class_='inq').string if li.find(class_='inq') is not None else '',
                    'playable':li.find(class_='playable').string if li.find(class_='playable') is not None else ''
                }

def write_to_json(data):

     if (float(data.get("score"))>9):
           print(data.get("title"))
     with open('./doubantop250.txt','a',encoding="utf-8") as file:
         file.write(json.dumps(data,ensure_ascii=False,indent=2))



def get_topN_data(page):
    for i in range(page):
        html = get_one_page(i*25)
        for info in get_one_page_data(html):
            write_to_json(info)
        time.sleep(1)

if __name__=='__main__':
    get_topN_data(10)



