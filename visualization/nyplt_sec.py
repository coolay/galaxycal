# encoding: utf-8

# !/usr/bin/env python

'''

@author: act'

@contact:2289818400@qq.com

@file: nyplt_sec.py

@time: 2018/5/29 20:00

@desc:
'''

import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl
#显示中文不乱码
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

x = np.linspace(-2, 2, 100)
y1 = np.cos(np.pi * x)
y2 = np.sin(np.pi*x)

plt.plot(x, y1, 'go',label=r"$y1=\cos(\pi \times x)$",alpha=0.8,linewidth=0.7)
plt.plot(x, y2, 'r-',label=r"$y2=\cos(\pi \times x)$",alpha=0.8,linewidth=0.7)

plt.annotate("important point",(0,1),xytext=(-1.5,1.1),arrowprops=dict(arrowstyle='->'))

plt.xlabel('x-axis')
plt.ylabel('y-axis')

plt.axis([-2.1,2.1,-1.2,1.2])

plt.legend()
plt.grid(alpha = 0.5)
plt.title("Two plots",color=(0.1,0.3,0.5))
plt.show()
