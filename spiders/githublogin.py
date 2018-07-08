# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: githublogin.py

@time: 2018/7/7 17:03

@desc:
'''

import requests
from bs4 import BeautifulSoup
import lxml
class Login(object):
    def __init__(self):
        self.headers={
            "Host":"github.com",
            "Referer":"https://github.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        }
        self.login_url = 'https://github.com/login'
        self.post_url = "https://github.com/session"
        self.logined_url = "https://github.com/settings/profile"
        self.session = requests.Session()

    def token(self):
        response = self.session.get(self.login_url,headers=self.headers)
        soup = BeautifulSoup(response.text,'lxml')
        input = soup.find(attrs={'name':'authenticity_token'})
        print(input)
        return input.attrs['value']


    def login(self):
        post_data={"utf8": "✓",
        "authenticity_token": self.token(),
        "login": "coolay",
        "password": "756536730chen",
        "commit": "Sign in"}
        print(post_data)
        response = self.session.post(self.post_url,data=post_data,headers = self.headers)
        print(response.status_code)
        print('login in ')
        response = self.session.get(self.logined_url,headers=self.headers)
        soup = BeautifulSoup(response.content,'lxml')
        # print(soup)
        for li in  soup.find_all(class_='js-selected-navigation-item menu-item'):
            print(li.string)


if __name__=='__main__':
    #login = Login()
   # login.login()
    post_data={"utf8": "✓",
        "authenticity_token": 'sdf',
        "login": "coolay",
        "password": "756536730chen",
        "commit": "Sign in"}

    response = requests.Session().post("http://httpbin.org/post",data=post_data)
    print(response.text)
    print('login in ')