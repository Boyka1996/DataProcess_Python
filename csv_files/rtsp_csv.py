#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/12/4 15:45
@Author     : Boyka
@Contact    : zhw@s.upc.edu.cn
@File       : rtsp_csv.py
@Project    : DataProcess_Python
@Description:
"""

import pandas as pd
import numpy as np
import csv
import xlrd
import yaml

xls_file = xlrd.open_workbook("1.xls")
print(type(xls_file))
table = xls_file.sheets()[0]
ip = table.col_values(0)
fire = table.col_values(6)
urls = []
for idx, item in enumerate(ip):
    if len(fire[idx]) > 0:
        rtsp_url = "rtsp://admin:ddfdc12345@" + item + ":554/h264/ch1/main/av_stream"
        print(rtsp_url)
        urls.append({"taskid": item, "id": idx, "rtsp": rtsp_url})
rtsp = {"rtsp": urls}
final_dict = {"person": rtsp}
with open("person_video_stream.yml", "w", encoding="utf-8") as f:
    yaml.dump(final_dict, f)
