#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/5/19 10:58
@Author     : Boyka
@Contact    : upcvagen@163.com
@File       : deaw1.py
@Project    : DataProcess_Python
@Description:
"""
import numpy as np
import matplotlib.pyplot as plt
import random

# 生成测试数据
# x = np.linspace(0, 10, 11)
# y = 11 - x
x = []
for _ in range(5):
    x.append(round(random.uniform(60, 80), 2))
x.append(85.13)
x.append(92.68)
x.append(93.16)
y = ['Client1', 'Client2', 'Client3', 'Client4', 'Client5', 'FedAvg', 'DFL', 'CT']
x=[76.86, 71.4, 65.53, 75.43, 70.62, 85.13, 92.68, 93.16]
print(y)
print(x)
# 绘制柱状图
plt.bar(y, x)
# plt.ylabel("Accuracy")
# plt.xlabel("Nodes")
# 循环，为每个柱形添加文本标注

# 居中对齐
for xx, yy in zip(y, x):
    plt.text(xx, yy + 0.2, str(yy), ha='center')

plt.show()
plt.savefig('1.png')