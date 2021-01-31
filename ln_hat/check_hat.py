#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/1/29 8:53
@Author     : Boyka
@Contact    : upcvagen@163.com
@File       : check_hat.py
@Project    : DataProcess_Python
@Description:
"""
import argparse
import json
import logging
import os
import xml.etree.cElementTree as ET
import numpy as np
import cv2


def convert_from_xml(xml_path):
    boxes = []
    try:
        tree = ET.ElementTree(file=xml_path)
    except:
        return []
    root = tree.getroot()
    obj_list = root.findall('object')
    for obj in obj_list:
        boxes.append([obj[0].text, int(obj[1][0].text), int(obj[1][1].text), int(obj[1][2].text), int(obj[1][3].text)])
    return boxes


def convert_from_json(json_path):
    boxes = []
    try:
        json_obj = json.load(open(json_path))
    except:
        return []
    obj_list = json_obj['shapes']
    for obj in obj_list:
        points = obj['points']
        points = np.array(points, np.int32)
        points = points.reshape(1, -1)[0]
        boxes.append([obj['label'], min(points[0::2]), min(points[1::2]), max(points[0::2]), max(points[1::2])])
    return boxes


if __name__ == '__main__':
    annotation_path="E:/Dataset/鲁能安全管控数据集/safety_helmet/safety_helmet/json"
    for annotation in os.listdir(annotation_path):
        annotation_file=os.path.join(annotation_path,annotation)
        bboxes=convert_from_json(annotation_file)
        for bbox in bboxes:
            if 'hat' not in bbox[0] and bbox[0]!='hair':
                print(annotation)
