# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: nyplt_f.py

@time: 2018/5/29 19:44

@desc:
'''

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2,2,100)
y = np.cos(np.pi*x)

plt.plot(x,y,'go')
plt.title("visualization first demo")
plt.show()