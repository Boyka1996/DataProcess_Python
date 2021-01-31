#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/1/30 12:14
@Author     : Boyka
@Contact    : upcvagen@163.com
@File       : convert_json_to_xml.py
@Project    : DataProcess_Python
@Description:
"""
import json
import numpy as np
import os
import xml.etree.ElementTree as ET
import cv2


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


# 增加换行符
def xml_indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            xml_indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def generate_xml(image, tar, bboxes):
    shape = cv2.imread(image)
    print(shape)
    annotation = ET.Element('annotation')

    tree = ET.ElementTree(annotation)

    size = ET.Element('size')
    width = ET.Element('width')
    height = ET.Element('width')
    width.text = str(shape[0])
    height.text = str(shape[1])
    size.append(width)
    size.append(height)

    for bbox in bboxes:
        obj = ET.Element('object')
        name = ET.Element('name')
        bndbox = ET.Element('bndbox')
        xmin = ET.Element('xmin')
        ymin = ET.Element('ymin')
        xmax = ET.Element('xmax')
        ymax = ET.Element('ymax')
        xmin.text = str(bbox[1])
        ymin.text = str(bbox[1])
        xmax.text = str(bbox[1])
        ymax.text = str(bbox[1])
        bndbox.append(xmin)
        bndbox.append(xmax)
        bndbox.append(ymin)
        bndbox.append(ymax)

        obj.append(name)
        obj.append(bndbox)
        annotation.append(obj)

    xml_indent(annotation)  # 增加换行符
    tree.write(tar, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    a = 'E:/Dataset/鲁能安全管控数据集/hat/images/1a6aaaa5e1c49a75e4df9d1825d61409.jpg'
    b = cv2.imread(a)
    print(b)
    c = b.shape
    print(b.shape)
    src = "E:/Dataset/鲁能安全管控数据集/hat/temp/Annotations"
    tar = "E:/Dataset/鲁能安全管控数据集/hat/temp/xml"
    img = "E:/Dataset/鲁能安全管控数据集/hat/temp/images"
    if not os.path.exists(tar):
        os.mkdir(tar)
    for annotation in os.listdir(src):
        src_annotation = os.path.join(src, annotation)
        boxes = convert_from_json(src_annotation)
        print(boxes)
        tar_annotation = os.path.join(tar, annotation.replace('.json', '.xml'))
        image_path = os.path.join(img, annotation.replace('.json', '.jpg'))
        print(image_path)
        generate_xml(image_path, tar_annotation, boxes)
