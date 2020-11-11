import argparse
import logging
import cv2
import numpy as np
import os
from mmdet.apis import inference_detector
from mmdet.apis import init_detector
import cv2
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='......%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def parse_args():
    parser = argparse.ArgumentParser(description='End-to-end inference')
    parser.add_argument(
        '--cfg',
        dest='cfg',
        help='cfg model file (/path/to/model_config.yaml)',
        default='/home/wzp/WZ2zp/mmdetection/configs/mask_rcnn/mask_rcnn_r101_fpn_1x_coco.py',
        type=str
    )
    parser.add_argument(
        '--wts',
        dest='wts',
        help='weights model file (/path/to/model_weights.pkl)',
        default='/home/wzp/WZ2zp/mmdetection/model/coco/mask_rcnn_r101_fpn_1x_coco_20200204-1efe0ed5.pth',
        type=str
    )
    parser.add_argument(
        '--srcImg',
        dest='srcImg',
        help='(/path/to/test/images)',
        default='/home/wzp/WZ2zp/mmdetection/tests/VOC2028/JPEGImages',
        type=str
    )
    parser.add_argument(
        '--src_xml',
        dest='src_xml',
        help='The location of xmls',
        default='/home/wzp/WZ2zp/mmdetection/tests/VOC2028/Annotations',
        type=str
    )
    parser.add_argument(
        '--tar_img',
        dest='tar_img',
        help='The location of xmls',
        default='/home/wzp/WZ2zp/mmdetection/tests/VOC2028/imgcut',
        type=str
    )
    parser.add_argument(
        '--tar_xml',
        dest='tar_xml',
        help='The location of xmls',
        default='/home/wzp/WZ2zp/mmdetection/tests/VOC2028/xml',
        type=str
    )
    return parser.parse_args()


def get_people(model, img):
    result = inference_detector(model, img)
    if isinstance(result, tuple):
        bbox_result, segm_result = result
    else:
        bbox_result, segm_result = result, None
    bboxes = np.vstack(bbox_result)
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(bbox_result)
    ]
    labels = np.concatenate(labels)
    result_bbox = []
    for bbox, label in zip(bboxes, labels):
        if bbox[4] < 0.8 and label > 0:
            continue
        # print(bbox[0:4])
        tmp = []
        for box in bbox[0:4]:
            tmp.append(int(box))
        result_bbox.append(tmp)
    print(result_bbox)
    return result_bbox


def get_hats(xml_path):
    tree = ET.ElementTree(file=xml_path)
    root = tree.getroot()
    hats = root.findall("object")
    hats_points = []
    for hat in hats:
        hat_point = []
        bndbox = hat.find("bndbox")
        hat_point.append(int(bndbox.find("xmin").text))
        hat_point.append(int(bndbox.find("ymin").text))
        hat_point.append(int(bndbox.find("xmax").text))
        hat_point.append(int(bndbox.find("ymax").text))
        hats_points.append(hat_point)
    return hats_points


def generate_xml(img_name, person_point, points, save_path):
    root_element = ET.Element("annotation")

    folder = ET.SubElement(root_element, "folder")
    folder.text = "UPC"
    filename = ET.SubElement(root_element, "filename")
    filename.text = img_name
    path = ET.SubElement(root_element, "path")
    path.text = "None"
    source = ET.SubElement(root_element, "source")
    database = ET.SubElement(source, "database")
    database.text = "Unknown"
    size = ET.SubElement(root_element, "size")

    width = ET.SubElement(size, "width")
    height = ET.SubElement(size, "height")
    depth = ET.SubElement(size, "depth")
    width.text = str(person_point[2] - person_point[0])
    height.text = str(person_point[3] - person_point[1])
    depth.text = "3"
    segmented = ET.SubElement(root_element, "segmented")
    segmented.text = "0"

    for point_id, point in enumerate(points):
        obj = ET.Element("object")
        name = ET.SubElement(obj, "name")
        pose = ET.SubElement(obj, "pose")
        truncated = ET.SubElement(obj, "truncated")
        difficult = ET.SubElement(obj, "difficult")
        name.text = "hat"
        pose.text = "Unspecified"
        truncated.text = "0"
        difficult.text = "Unknown"

        bndbox = ET.SubElement(obj, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        ymin = ET.SubElement(bndbox, "ymin")
        xmax = ET.SubElement(bndbox, "xmax")
        ymax = ET.SubElement(bndbox, "ymax")
        xmin.text = str(max(0, point[0] - person_point[0]))
        ymin.text = str(max(0, point[1] - person_point[1]))
        xmax.text = str(min(person_point[2], point[2] - person_point[2]))
        ymax.text = str(min(person_point[3], point[3] - person_point[3]))
        root_element.append(obj)
    # width = ET.SubElement(size, "width")
    # height = ET.SubElement(size, "height")
    # depth = ET.SubElement(size, "depth")
    # width.text = person_point[2] - person_point[0]
    # height.text = person_point[3] - person_point[1]
    # depth.text = 3
    # segmented = ET.SubElement(root_element, "segmented")
    # segmented.text = 0
    #
    # for point_id, point in enumerate(points):
    #     obj = ET.Element("object")
    #     name = ET.SubElement(obj, "name")
    #     pose = ET.SubElement(obj, "pose")
    #     truncated = ET.SubElement(obj, "truncated")
    #     difficult = ET.SubElement(obj, "difficult")
    #     name.text = "hat"
    #     pose.text = "Unspecified"
    #     truncated.text = 0
    #     difficult.text = "Unknown"
    #
    #     bndbox = ET.SubElement(obj, "bndbox")
    #     xmin = ET.SubElement(bndbox, "xmin")
    #     ymin = ET.SubElement(bndbox, "ymin")
    #     xmax = ET.SubElement(bndbox, "xmax")
    #     ymax = ET.SubElement(bndbox, "ymax")
    #     xmin.text = max(0, point[0] - person_point[0])
    #     ymin.text = max(0, point[1] - person_point[1])
    #     xmax.text = min(person_point[2], point[2] - person_point[2])
    #     ymax.text = min(person_point[3], point[3] - person_point[3])
    # 创建xml树，并将根节点放入其中
    xml_string = ET.tostring(root_element)

    dom = minidom.parseString(xml_string)
    with open(save_path, 'w', encoding='utf-8') as f:
        # indent为根节点缩进，newl每行数据句末符号，addindent为其他节点缩进
        dom.writexml(f, indent='\t', newl='\n',
                     addindent='\t', encoding='utf-8')


if __name__ == '__main__':
    args = parse_args()
    model = init_detector(args.cfg, args.wts, device='cuda:0')
    if not os.path.exists(args.tar_img):
        os.mkdir(args.tar_img)
    if not os.path.exists(args.tar_xml):
        os.mkdir(args.tar_xml)
    count = 0
    for image in os.listdir(args.srcImg):
        cv_img = cv2.imread(os.path.join(args.srcImg, image))
        people_list = get_people(model, cv_img)
        try:
            hat_list = get_hats(os.path.join(args.src_xml, image.replace('.jpg', '.xml')))
        except:
            hat_list = get_hats(os.path.join(args.src_xml, image.replace('.JPG', '.xml')))
        for person_id, person in enumerate(people_list):
            try:

                sub_img_name = image.replace('.jpg', '') + '_' + str(person_id) + '.jpg'
            except:
                sub_img_name = image.replace('JPG', '') + '_' + str(person_id) + '.jpg'
            sub_img = cv_img[person[1]:person[3], person[0]:person[2]]
            cv2.imwrite(os.path.join(args.tar_img, sub_img_name), sub_img)
            count += 1
            sub_hat_list = []
            for hat in hat_list:

                if (hat[0] + hat[2]) > person[0] and (hat[0] + hat[2]) < person[2] and (hat[1] + hat[3]) > person[
                    1] and (hat[1] + hat[3]) > person[3]:
                    sub_hat_list.append(hat)
            if len(sub_hat_list) == 0:
                continue
            generate_xml(img_name=sub_img_name, person_point=person, points=sub_hat_list,
                         save_path=os.path.join(args.tar_xml,
                                                image.replace('.jpg', '') + '_' + str(person_id) + '.xml'))
        print(count)
