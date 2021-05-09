# -*- coding: utf-8 -*-
# 返回各个类别的数目
import os
import json
import xml.etree.cElementTree as ET
import argparse
import logging
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--imagepath',
        dest='imagePath',
        default='K:/datasets/鲁能宁夏项目/鲁能标记螺母small/images',
        help='图片路径',
        type=str
    )
    parser.add_argument(
        '--xmlPath',
        dest='xmlPath',
        default='K:/datasets/鲁能宁夏项目/鲁能标记螺母small/Annotations',
        help='xml路径如果没有的话那就是None',
        type=str
    )
    parser.add_argument(
        '--jsonPath',
        dest='jsonPath',
        default='None',
        help='json路径,如果没有的话那就是None',
        type=str
    )
    parser.add_argument(
        '--savePath',
        dest='savePath',
        default='None',
        help='保存图片路径,如果不要那就直接是None',
        type=str
    )
    return parser.parse_args()


def main(args):
    print(args)
    # xmlOfImage=None
    # jsonOfImage=None
    class_dict = {}
    image_dict = {'图片总数': len(os.listdir(args.imagePath)), 'xml和json都有': 0, '只有xml': 0, '只有json': 0, '都没有': 0}
    for img in os.listdir(args.imagePath):
        imageFile = os.path.join(args.imagePath, img)
        xmlOfImage = os.path.join(args.xmlPath, img.replace('.jpg', '.xml'))
        jsonOfImage = os.path.join(args.jsonPath, img.replace('.jpg', '.json'))
        if os.path.exists(xmlOfImage) and os.path.exists(jsonOfImage):
            image_dict['xml和json都有'] += 1
        elif os.path.exists(xmlOfImage) and not os.path.exists(jsonOfImage):
            image_dict['只有xml'] += 1
        elif not os.path.exists(xmlOfImage) and os.path.exists(jsonOfImage):
            image_dict['只有json'] += 1
        else:
            image_dict['都没有'] += 1
    if args.xmlPath != None:
        for xmlFile in os.listdir(args.xmlPath):
            if not os.path.exists(os.path.join(args.imagePath, xmlFile.replace('.xml', '.jpg'))):
                continue
            tree = ET.parse(os.path.join(args.xmlPath, xmlFile))
            root = tree.getroot()
            for obj in root:
                if obj.tag == 'object':
                    objName = obj[0].text
                    if not objName in class_dict.keys():
                        class_dict[objName] = 1
                    else:
                        class_dict[objName] += 1
        print("xml文件统计完毕！")
    if args.jsonPath != 'None':
        for jsonFile in os.listdir(args.jsonPath):
            if not os.path.exists(os.path.join(args.imagePath, jsonFile.replace('.json', '.jpg'))):
                continue
            jsonObj = json.load(open(os.path.join(args.jsonPath + jsonFile)))
            objs = jsonObj['shapes']
            for obj in objs:
                if not obj['label'] in class_dict.keys():
                    # if not class_dict.has_key(objName):
                    class_dict[obj['label']] = 1
                else:
                    class_dict[obj['label']] += 1
        print("json文件统计完毕！")
    print(image_dict)
    # print(class_dict)
    image_dict_class_list, image_dict_num_list = convert_and_sort(image_dict)
    class_list, class_num = convert_and_sort(class_dict)
    if args.savePath is not 'None':
        saveAsImage(class_list, class_num, os.path.join(args.savePath, 'class_statistics.jpg'))
        # saveAsImage(image_dict_class_list,image_dict_num_list,os.path.join(args.savePath,'images_statistics.jpg'))


def convert_and_sort(myDict):
    keyList = []
    valueList = []
    L = list(myDict.items())
    L.sort(key=lambda x: x[1], reverse=False)
    print(L)
    for i in L:
        keyList.append(i[0])
        valueList.append(i[1])
    return keyList, valueList


def saveAsImage(x, y, saveName):
    _x = range(len(x))
    plt.xlabel('num', fontsize=18)
    plt.ylabel('label', fontsize=18)
    plt.title('Label Statistics', fontsize=18)
    # _x=[2,3,4,5,7,10,11,12,13,14,15,17]
    plt.barh(_x, y, tick_label=x)
    for item_x, item_y in zip(_x, y):
        plt.text(item_y + 100, item_x - 0.3, '%d' % item_y, ha='center', va='bottom')
    # plt.savefig(saveName)
    plt.show()


if __name__ == '__main__':
    args = parse_args()
    main(args)
