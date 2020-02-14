#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draw the annotations(including the xml and json files ) on the original images to view the annotating effect
"""
import numpy as np
import cv2
import os
import json
import xml.etree.cElementTree as ET


def drawxml(xmlpath, im):
    tree = ET.ElementTree(file=xmlpath)
    print("resoluting...")
    root = tree.getroot()
    for obj in root:
        if obj.tag == 'object':
            objectname = obj[0].text  # object name
            box = []
            print('name:' + objectname)
            for bndbox in obj:
                for sub in bndbox:
                    box.append(int(sub.text))  # bndbox
            box = np.array(box)
            print(box)
            cv2.rectangle(im, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(im, 'label:' + objectname, (box[0], box[1]), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    return im


def drawjson(jsonpath, im):
    jsonobj = json.load(open(jsonpath))
    objs = jsonobj['shapes']
    for obj in objs:
        boxes = obj['points']
        pts = np.array(boxes, np.int32)
        pts = pts.reshape((-1, 1, 2))
        print(pts)
        objectname = obj['label']
        cv2.polylines(im, [pts], True, (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(im, 'label:' + objectname, (pts[0][0][0], pts[0][0][1]), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return im


if __name__ == '__main__':
    imgpath = "/media/chase/4b745c9a-63fb-4f92-a911-ab31c54841d0/chase/LNDataset/围栏temp/images/"
    xmlpath = ""
    drawjsonpath = "/media/chase/4b745c9a-63fb-4f92-a911-ab31c54841d0/chase/LNDataset/围栏temp/draw/"
    drawxmlpath = ""
    jsonpath = "/media/chase/4b745c9a-63fb-4f92-a911-ab31c54841d0/chase/LNDataset/围栏temp/json/"
    for f in os.listdir(imgpath):
        im = cv2.imread(imgpath + f)
        jsonName = jsonpath + f.replace(".jpg", ".json")
        xmlName = xmlpath + f.replace(".jpg", ".xml")
        print((jsonName))
        if os.path.exists(jsonName):
            jsondrawed = drawjson(jsonName, im)
            cv2.imwrite(drawjsonpath + f, jsondrawed)
            print(drawjsonpath + f)
        if os.path.exists(xmlName):
            xmldrawed = drawxml(xmlName, im)
            cv2.imwrite(drawxmlpath)
