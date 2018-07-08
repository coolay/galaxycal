# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: unsplash.py

@time: 2018/6/30 11:23

@desc:
'''

import requests
import json
import time
from contextlib import closing

class Unsplash(object):

    def __init__(self,headers=None,photosPaths = None):
        if photosPaths is None:
            self.photosPaths = []
        else:
            self.photosPaths = photosPaths
        self.headers = headers
        self.downloadUrl = "https://unsplash.com/photos/xxx/download?force=true"

    def get_page_photoPath(self,url):
        response = requests.get(url=url,headers = self.headers)
        dataJson = json.loads(response.text)

        for item in dataJson:
            self.photosPaths.append( item.get('id'))

        time.sleep(1)

    def down_photos(self):
        print(self.photosPaths)
        print("图片开始下载.......")
        i = 1
        for id in self.photosPaths:
            print("正在下载第%d张......."%i)
            targetDownloadPath =  self.downloadUrl.replace('xxx',id)
            with closing(requests.get(url=targetDownloadPath,headers = self.headers) )as r:
                with open('D:/spiderstempfile/unsplashphoto/%s.jpg'%id,'ab+') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
            time.sleep(1)
            i+=1


if __name__=='__main__':

    photosUrl = "https://unsplash.com/napi/photos?per_page=12&order_by=latest&page="
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
    unplash = Unsplash(headers = headers,photosPaths=[])
    for x in range(3,5):
        unplash.get_page_photoPath(photosUrl+str(x))

    unplash.down_photos()
