#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/5/19 17:04
@Author     : Boyka
@Contact    : upcvagen@163.com
@File       : draw2.py
@Project    : DataProcess_Python
@Description:
"""

# -*- coding:utf-8 -*-
# ! python3
import random

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d


# 定义函数来显示柱状上的数值
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%s' % float(height))


if __name__ == '__main__':
    # for _ in range(5):
    #     x.append(round(random.uniform(60, 80), 2))
    l1 = [68, 96, 85, 86, 76, 87, 95, 100]
    l2 = [85, 68, 79, 89, 94, 82, 90, 95]
    l3 = [68, 96, 85, 86, 76, 87, 95, 100]
    l4 = [85, 68, 79, 89, 94, 82, 90, 100]
    l5 = [68, 96, 85, 86, 76, 87, 95, 100]
    l6 = [85, 68, 79, 89, 94, 82, 90, 100]
    l7 = [68, 96, 85, 86, 76, 87, 95, 100]
    l8 = [68, 96, 85, 86, 76, 87, 95, 100]
    name = ['Client1', 'Client2', 'Client3', 'Client4', 'Client5', 'FedAvg', 'DFL', 'CT']
    total_width, n = 4.2, 7
    width = 0.1
    x = [0, 1, 2, 3, 4, 5, 6,7]
    plt.rc('font', family='SimHei', size=12)  # 设置中文显示，否则出现乱码！
    a = plt.bar(x, l1, width=width, label='数学', fc='y')
    for i in range(len(x)):
        x[i] = x[i] + width
    b = plt.bar(x, l2, width=width, label='语文', tick_label=name, fc='r')
    for i in range(len(x)):
        x[i] = x[i] + width
    c = plt.bar(x, l3, width=width, label='语文', tick_label=name, fc='r')
    for i in range(len(x)):
        x[i] = x[i] + width
    d = plt.bar(x, l3, width=width, label='语文', tick_label=name, fc='r')
    for i in range(len(x)):
        x[i] = x[i] + width
    e = plt.bar(x, l3, width=width, label='语文', tick_label=name, fc='r')
    for i in range(len(x)):
        x[i] = x[i] + width
    f = plt.bar(x, l3, width=width, label='语文', tick_label=name, fc='r')
    for i in range(len(x)):
        x[i] = x[i] + width
    g = plt.bar(x, l3, width=width, label='语文', tick_label=name, fc='r')
    # for i in range(len(x)):
    #     x[i] = x[i] + width
    # h = plt.bar(x, l3, width=width, label='语文', tick_label=name, fc='r')
    # b = plt.bar(x, l2, width=width, label='语文', tick_label=name, fc='r')
    # b = plt.bar(x, l2, width=width, label='语文', tick_label=name, fc='r')
    # b = plt.bar(x, l2, width=width, label='语文', tick_label=name, fc='r')
    autolabel(a)
    autolabel(b)
    autolabel(c)
    autolabel(d)
    autolabel(e)
    autolabel(f)
    autolabel(g)
    # autolabel(h)

    plt.xlabel('学生')
    plt.ylabel('成绩')
    plt.title('学生成绩')
    plt.legend()
    plt.show()
