#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2020/11/23 9:54
@Author     : Boyka
@Contact    : upcvagen@163.com
@File       : generate_result_csv.py
@Project    : DataProcess_Python
@Description:
"""
import csv


def init_model():
    """
    加载模型
    :return:
    """
    pass


def detect():
    """
    利用模型检测图片
    :return:[图片名，类别，置信度，xmin,ymin,xmax,ymax,类别，置信度，xmin,ymin,xmax,ymax,类别，置信度，xmin,ymin,xmax,ymax......]
    """
    pass


def generate_csv():
    """
    将detect检测到的结果逐行保存到csv
    :return:
    """
    data = [['1.jpg', 'redhat', 0.615, 10, 10, 100, 10, 'class', 0.6, 10, 10, 100, 100],
            ['greenhat', 'class', 0.953, 10, 10, 100, 10, 'class', 0.6, 10, 10, 100, 100]]
    with open("./result_sample.csv", "a", newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow(item)


if __name__ == '__main__':
    generate_csv()
