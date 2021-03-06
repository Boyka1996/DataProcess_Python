from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import argparse
import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
import glob
import logging
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from caffe2.python import workspace

from detectron.core.config import assert_and_infer_cfg
from detectron.core.config import cfg
from detectron.core.config import merge_cfg_from_file
from detectron.utils.io import cache_url
from detectron.utils.logging import setup_logging
from detectron.utils.timer import Timer
import detectron.core.test_engine as infer_engine
import detectron.utils.c2 as c2_utils
import xml.etree.cElementTree as ET
import json
import os

c2_utils.import_detectron_ops()
# OpenCL may be enabled by default in OpenCV3; disable it because it's not
# thread safe and causes unwanted GPU memory allocations.
cv2.ocl.setUseOpenCL(False)
class_precision_dict = {}  # 格式{类别：[真实目标数,检测到的目标数,检测对的目标数,误检目标数,漏检目标数,准确率,召回率]}


def parse_args():
    parser = argparse.ArgumentParser(description='End-to-end inference')
    parser.add_argument(
        '--cfg',
        dest='cfg',
        help='cfg model file (/path/to/model_config.yaml)',
        default='/home/chase/project/LNOnsiteMonitor/model/models/belt/e2e_mask_rcnn_R-101-FPN_2x.yaml',
        type=str
    )
    parser.add_argument(
        '--wts',
        dest='weights',
        help='weights model file (/path/to/model_weights.pkl)',
        default='/home/chase/project/LNOnsiteMonitor/model/models/belt/model_final.pkl',
        type=str
    )
    parser.add_argument(
        '--srcImg',
        dest='srcImg',
        help='(/path/to/test/images)',
        default='/home/chase/Boyka/test/images',
        type=str
    )
    parser.add_argument(
        '--xml',
        dest='xml',
        help='The location of xmls',
        default='/home/chase/Boyka/test/Annotations',
        type=str
    )
    parser.add_argument(
        '--json',
        dest='json',
        help='The location of jsons ',
        default=None,
        type=str
    )
    parser.add_argument(
        '--dataset',
        dest='dataset',
        help='The location of annotations',
        default=['_background_(这个不要改)', 'belt'],
        # default=['_background_(这个不要改)', 'redhat', 'yellowhat', 'greenhat', 'bluehat', 'whitehat', 'red', 'yellow', 'orange', 'blue',
        # 'green', 'lightgreen', 'belt'],
        type=list
    )
    parser.add_argument(
        '--thresh',
        dest='thresh',
        help='交幷比阈值',
        default=0.5,
        type=float
    )
    parser.add_argument(
        '--draw_path',
        dest='draw_path',
        help='画图路径，如果不要画出来那就是None',
        default='/home/chase/Boyka/1',
        type=str
    )

    return parser.parse_args()


def convert_from_xml(xmlpath):
    bboxes = []
    try:
        tree = ET.ElementTree(file=xmlpath)
    except:
        return []
    root = tree.getroot()
    objList = root.findall('object')
    for obj in objList:
        bboxes.append((obj[0].text, int(obj[1][0].text), int(obj[1][1].text), int(obj[1][2].text), int(obj[1][3].text)))
    return bboxes


def convert_from_json(jsonPath):
    bboxes = []
    try:
        jsonobj = json.load(open(jsonPath))
    except:
        return []
    objs = jsonobj['shapes']
    for obj in objs:
        pts = obj['points']
        pts = np.array(pts, np.int32)
        pts = pts.reshape(1, -1)[0]
        xmin = min(pts[0::2])
        ymin = min(pts[1::2])
        xmax = max(pts[0::2])
        ymax = max(pts[1::2])
        bboxes.append((obj['label'], xmin, ymin, xmax, ymax))
    return bboxes


def convert_from_cls_format(cls_boxes):
    """Convert from the class boxes/segms/keyps format generated by the testing
    code.
    """
    box_list = [b for b in cls_boxes if len(b) > 0]
    if len(box_list) > 0:
        boxes = np.concatenate(box_list)
    else:
        boxes = None

    classes = []
    for j in range(len(cls_boxes)):
        classes += [j] * len(cls_boxes[j])
    return boxes, classes


def vis_one_image(boxes, thresh=0.7):
    """Visual debugging of detections."""
    result_box = []
    if isinstance(boxes, list):
        boxes, classes = convert_from_cls_format(boxes)
    if boxes is None or boxes.shape[0] == 0 or max(boxes[:, 4]) < thresh:
        return []

    # Display in largest to smallest order to reduce occlusion
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    sorted_inds = np.argsort(-areas)

    for i in sorted_inds:
        bbox = boxes[i, :4]
        score = boxes[i, -1]
        if score < thresh:
            continue
        result_box.append((args.dataset[classes[i]], int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])))
    return result_box


def gtBboxesToClassDict(gtBboxes):
    for gtBbox in gtBboxes:
        if not gtBbox[0] in class_precision_dict.keys():
            class_precision_dict[gtBbox[0]] = [1, 0, 0, 0, 0, 0, 0]
        else:
            class_precision_dict[gtBbox[0]][0] += 1
def preBboxesToClassDict(gtBboxes):
    for gtBbox in gtBboxes:
        if not gtBbox[0] in class_precision_dict.keys():
            class_precision_dict[gtBbox[0]] = [0, 1, 0, 0, 0, 0, 0]
        else:
            class_precision_dict[gtBbox[0]][1] += 1


def compare(im, bboxes, name):
    gtBboxes = []
    true_detection = 0
    false_detection = 0
    missing_detection = 0
    if args.xml != None:
        gtBboxes.extend(convert_from_xml(os.path.join(args.xml, name + '.xml')))
    if args.json != None:
        gtBboxes.extend(convert_from_json(os.path.join(args.json, name + '.json')))
    # print(gtBboxes)
    gtBboxesToClassDict(gtBboxes)
    # if args.draw_path is not None:
    #     draw_bboxes(im, gtBboxes, name, True)
    ground_truth_num = len(gtBboxes)
    predicted_num = len(bboxes)
    if gtBboxes==[] and bboxes!=None:
        for bbox in bboxes:
            class_precision_dict[bbox[0]][3]+=1
            false_detection+=1
    for gt in gtBboxes:
        ifMissed=True
        for pre in bboxes:
            if gt[0] == pre[0] and IoU(gt, pre) > args.thresh:
                class_precision_dict[gt[0]][2]+=1
                true_detection += 1
                # print('=================')
                # print(bboxes,gtBboxes)
                bboxes.remove(pre)
                # print(bboxes,gtBboxes)
                # print('=================')
                ifMissed=False
                continue
        if ifMissed:
            class_precision_dict[gt[0]][4]+=1
            missing_detection+=1
        for bbox in bboxes:
            class_precision_dict[bbox[0]][3]+=1
            false_detection+=1
    # missing_detection = ground_truth_num - true_detection
    # false_detection = predicted_num - true_detection
    return ground_truth_num, predicted_num, true_detection, false_detection, missing_detection


def IoU(bbox1, bbox2):
    inter_rect_xmin = max(bbox1[1], bbox2[1])
    inter_rect_ymin = max(bbox1[2], bbox2[2])
    inter_rect_xmax = min(bbox1[3], bbox2[3])
    inter_rect_ymax = min(bbox1[4], bbox2[4])
    inter_area = max(0, (inter_rect_xmax - inter_rect_xmin)) * max(0, (inter_rect_ymax - inter_rect_ymin))
    area1 = (bbox1[3] - bbox1[1]) * (bbox1[4] - bbox1[2])
    area2 = (bbox2[3] - bbox2[1]) * (bbox2[4] - bbox2[2])
    iou = inter_area / (area1 + area2 - inter_area)
    return iou


def draw_bboxes(im, bboxes, name, type):
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    COLOR = RED
    if type:
        COLOR = GREEN
        # print('gt')
    if bboxes != []:
        font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
        for bbox in bboxes:
            cv2.rectangle(im, (bbox[1], bbox[2]), (bbox[3], bbox[4]), COLOR, thickness=2)
            cv2.putText(im, bbox[0], (bbox[1], bbox[2]), font, 0.6, COLOR, 2)
    cv2.imwrite(os.path.join(args.draw_path, name + '.jpg'), im)
def draw_statistics(keyList,precisionList,recallList):
    print(keyList,precisionList,recallList)
    _x = list(range(len(keyList)))
    plt.xlabel('precison&recall', fontsize=18)
    plt.ylabel('label', fontsize=18)
    plt.title('Precison Statistics', fontsize=18)
    total_width,n=0.8,2
    width=total_width/n
    pre=plt.bar(_x,precisionList,width=width,label='precision',tick_label='',fc='y')
    for i in range(len(_x)):
        _x[i]+=width
    plt.bar(_x,recallList,width=width,label='recall',tick_label='',fc='r')
    # # _x=[2,3,4,5,7,10,11,12,13,14,15,17]
    # plt.barh(_x, precisionList, tick_label=keyList)
    # for item_x, item_y in zip(_x, precisionList):
    #     plt.text(item_y + 100, item_x - 0.3, '%.2f' % item_y, ha='center', va='bottom')
    plt.legend()
    for i in range(len(keyList)):
        plt.text(i+0.155,-1,keyList[i],rotation=25)


    plt.savefig('./2.jpg')
    plt.show()
def convertFromDict(myDict):
    keyList=[]
    precisionList=[]
    recallList=[]
    for i in myDict:
        keyList.append(i)
        precisionList.append(myDict[i][5])
        recallList.append(myDict[i][6])
    return keyList,precisionList,recallList

def main(args):
    logger = logging.getLogger(__name__)
    merge_cfg_from_file(args.cfg)
    cfg.TEST.WEIGHTS = args.weights

    cfg.NUM_GPUS = 1
    thresh = 0.7
    assert_and_infer_cfg()
    model = infer_engine.initialize_model_from_cfg(args.weights)
    model_precision_statistics={'ground_truth':0,'detected_obj':0,'true_detection':0,'false_detection':0,'missing_detection':0,'precision':0,'recall':0}
    for image in os.listdir(args.srcImg):
        try:
            im = cv2.imread(os.path.join(args.srcImg, image))
            with c2_utils.NamedCudaScope(0):
                cls_boxes, cls_segms, cls_keyps = infer_engine.im_detect_all(
                    model, im, None, None
                )
                bboxes = vis_one_image(cls_boxes, 0.8)
                preBboxesToClassDict(bboxes)
                # print(bboxes)
        except:
            print('获取检测结果的时候歇逼了')
        try:
            if args.draw_path != None:
                if not os.path.exists(args.draw_path):
                    os.makedirs(args.draw_path)
                draw_bboxes(im, bboxes, image.split('.')[0], False)
            g, d, t, f, m = compare(im, bboxes, image.split('.')[0])
            # print(class_precision_dict)

            # print(g, d, t, f, m)
            model_precision_statistics['ground_truth'] += g
            model_precision_statistics['detected_obj'] += d
            model_precision_statistics['true_detection'] += t
            model_precision_statistics['false_detection'] += f
            model_precision_statistics['missing_detection'] += m
        except:
            print('验证的时候歇逼了')
    model_precision_statistics['precision']=model_precision_statistics['true_detection']*100/model_precision_statistics['detected_obj']
    model_precision_statistics['recall']=model_precision_statistics['true_detection']*100/model_precision_statistics['ground_truth']
    for single_class in class_precision_dict:
        class_precision_dict[single_class][5]=class_precision_dict[single_class][2]*100/class_precision_dict[single_class][1]
        class_precision_dict[single_class][6] = class_precision_dict[single_class][2] * 100 /class_precision_dict[single_class][0]
    print(model_precision_statistics)
    print(class_precision_dict)
    print("测试图片数：    %d" % len(os.listdir(args.srcImg)))
    print("真实目标数：    %d" % model_precision_statistics['ground_truth'])
    print("检测到的目标数： %d" % model_precision_statistics['detected_obj'])
    print("检测对的目标数： %d" % model_precision_statistics['true_detection'])
    print("误检目标数：    %d" % model_precision_statistics['false_detection'])
    print("漏检目标数：    %d" % model_precision_statistics['missing_detection'])
    print("准确率：       %f%%" % model_precision_statistics['precision'])
    print("召回率：       %f%%" % model_precision_statistics['recall'])
    classes,precision,recall=convertFromDict(class_precision_dict)
    draw_statistics(classes,precision,recall)


if __name__ == '__main__':
    workspace.GlobalInit(['caffe2', '--caffe2_log_level=0'])
    setup_logging(__name__)
    args = parse_args()
    main(args)
