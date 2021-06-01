#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/5/20 9:00
@Author     : Boyka
@Contact    : upcvagen@163.com
@File       : data.py
@Project    : DataProcess_Python
@Description:
"""
import csv
import random

# 1. 创建文件对象
f = open("文件名.csv", 'w', encoding="utf-8", newline="")

# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(f)

# 3. 构建列表头
a = [76.86, 71.4, 65.53, 75.43, 70.62, 85.13, 92.68, 93.16]

# 4. 写入csv文件内容
csv_writer.writerow([round(i - random.uniform(20, 30), 2) for i in a])
csv_writer.writerow([round(i - random.uniform(10, 20), 2) for i in a])
csv_writer.writerow([round(i - random.uniform(5, 10), 2) for i in a])
csv_writer.writerow([round(i - random.uniform(0, 5), 2) for i in a])
csv_writer.writerow(a)
# 5. 关闭文件
f.close()
