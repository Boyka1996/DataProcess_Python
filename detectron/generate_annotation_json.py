# -*- coding: utf-8 -*-
# School                 ：UPC
# Author                 ：Boyka
# File Name              ：generate_annotation_json.py
# Computer User          ：Administrator 
# Current Project        ：DataProcess_Python
# Development Time       ：2020/2/19  21:53 
# Development Tool       ：PyCharm
import argparse
import json
import logging
import os
import xml.etree.cElementTree as eT
import cv2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image_path',
        dest='image_path',
        default='F:datasets/LNSafetyControl/safety_helmet/safety_helmet/images/',
        help='图片路径',
        type=str
    )
    parser.add_argument(
        '--xml_path',
        dest='xml_path',
        default='F:datasets/LNSafetyControl/safety_helmet/safety_helmet/xml/',
        help='xml路径如果没有的话那就是None',
        type=str
    )
    parser.add_argument(
        '--json_path',
        dest='json_path',
        default='F:datasets/LNSafetyControl/safety_helmet/safety_helmet/json/',
        help='json路径,如果没有的话那就是None',
        type=str
    )
    parser.add_argument(
        '--classes',
        dest='classes',
        default=['redhat', 'yellowhat', 'bluehat', 'whitehat', 'blackhat', 'hair', '', '', '', '', ''],
        help='保存图片路径,如果不要那就直接是None',
        type=list
    )
    parser.add_argument(
        '--classes_mapping',
        dest='classes_mapping',
        default=None,
        help='保存图片路径,如果不要那就直接是None',
        type=str
    )
    parser.add_argument(
        '--save_path',
        dest='save_path',
        default='F:datasets/LNSafetyControl/safety_helmet/safety_helmet/safety_helmet.json',
        help='保存图片路径,如果不要那就直接是None',
        type=str
    )

    return parser.parse_args()


def get_xml_objects(xml_path_, annotation_info_):
    object_id = annotation_info_.get("object_id")
    category_count = annotation_info_.get("category_count")

    xml_annotations = []
    tree = eT.ElementTree(file=xml_path_)
    root = tree.getroot()
    for obj in root:
        if obj.tag == 'object':
            if obj[0].text in category_count:
                category_count[obj[0].text] += 1
            else:
                category_count[obj[0].text] = 1

            if obj[0].text in annotation_info_.get("categories"):
                category_id = annotation_info_.get("categories").index(obj[0].text) + 1
            elif obj[0].text in annotation_info_.get("category_mapping").keys():
                category_id = annotation_info_.get("categories").index(
                    annotation_info_.get("category_mapping").get(obj[0].text)) + 1
            else:
                continue
            xmin = int(obj[1][0].text)
            ymin = int(obj[1][1].text)
            xmax = int(obj[1][2].text)
            ymax = int(obj[1][3].text)
            xml_annotations.append(
                {"segmentation": [[xmin, ymin, xmax, ymin, xmax, ymax, ymin, ymax]],
                 "area": (xmax - xmin) * (ymax - ymin),
                 "iscrowd": 0,
                 "image_id": annotation_info_.get("image_id"),
                 "bbox": [xmin, ymin, xmax - - xmin, ymax - ymin],
                 "category_id": category_id,
                 "id": object_id})
            object_id += 1
    return xml_annotations, object_id, category_count


def get_json_objects(json_path_, annotation_info_):
    object_id = annotation_info_.get("object_id")
    category_count = annotation_info_.get("category_count")

    json_annotations = []
    json_obj = json.load(open(json_path_))
    objects = json_obj['shapes']
    for obj in objects:
        if obj['label'] in category_count:
            category_count[obj['label']] += 1
        else:
            category_count[obj['label']] = 1

        if obj['label'] in annotation_info_.get("categories"):
            category_id = annotation_info_.get("categories").index(obj['label']) + 1
        elif obj['label'] in annotation_info_.get("category_mapping").keys():
            category_id = annotation_info_.get("categories").index(
                annotation_info_.get("category_mapping").get(obj['label'])) + 1
        else:
            continue

        points = obj['points']
        x_coordinates_points = [x_coordinates_point[0] for x_coordinates_point in points]
        y_coordinates_points = [y_coordinates_point[-1] for y_coordinates_point in points]
        segmentation = []
        for point in points:
            segmentation = segmentation + point
        xmin = min(x_coordinates_points)
        ymin = min(y_coordinates_points)
        xmax = max(x_coordinates_points)
        ymax = max(y_coordinates_points)

        json_annotations.append(
            {"segmentation": [segmentation],
             "area": (xmax - xmin) * (ymax - ymin),
             "iscrowd": 0,
             "image_id": annotation_info_.get("image_id"),
             "bbox": [xmin, ymin, xmax - - xmin, ymax - ymin],
             "category_id": category_id,
             "id": object_id})
        object_id += 1

    return json_annotations, object_id, category_count


def get_categories(super_categories, categories):
    categories_result = []
    for category_id, category in enumerate(categories):
        if len(super_categories) == len(categories):
            categories_result.append(
                {"supercategory": super_categories[category_id], "id": category_id + 1, "name": category})
        else:
            categories_result.append(
                {"supercategory": category, "id": category_id + 1, "name": category})
    return categories_result


def get_image_info(image_path_, image_id_):
    image_shape = cv2.imread(image_path_).shape
    return {"license": 0, "file_name": os.path.basename(image_path_), "coco_url": "", "height": image_shape[0],
            "width": image_shape[1], "date_captured": "", "flickr_url": "", "id": image_id_}


def generate_annotation(args_):
    image_path = args_.image_path
    xml_path = args_.xml_path
    json_path = args_.json_path
    save_path = args_.save_path
    if args_.classes_mapping:
        category_mapping = eval(args_.classes_mapping)
    else:
        category_mapping = {}

    logger.info(save_path)

    info = {}
    licenses = []
    images = []
    annotations = []
    categories = get_categories(args_.classes, args_.classes)

    image_id = 1
    object_id = 1
    category_count = {}

    for image_name in os.listdir(image_path):
        annotation_info = {
            "image_id": image_id,
            "object_id": object_id,
            "categories": args_.classes,
            "category_mapping": category_mapping,
            "category_count": category_count
        }
        if_labeled = False
        if xml_path:
            xml_file = os.path.join(xml_path, image_name.replace('.jpg', '.xml'))
            if os.path.exists(xml_file):
                if_labeled = True
                xml_objects, object_id, category_count = get_xml_objects(xml_file, annotation_info)
                annotations = annotations + xml_objects
        if json_path:
            json_file = os.path.join(json_path, image_name.replace('.jpg', '.json'))
            if os.path.exists(json_file):
                if_labeled = True
                json_objects, object_id, category_count = get_json_objects(json_file, annotation_info)
                annotations = annotations + json_objects
        if if_labeled:
            logger.info(image_name)
            image_id += 1
            image_info = get_image_info(os.path.join(image_path, image_name), image_id)
            images.append(image_info)
    data_set_annotation = {"info": info, "licenses": licenses, "images": images, "annotations": annotations,
                           "categories": categories}
    with open(save_path, 'w') as f:
        logger.info(save_path)
        f.write(json.dumps(data_set_annotation))
        logger.info("***********************************")
        logger.info(category_count)


if __name__ == '__main__':
    path_args = parse_args()
    generate_annotation(path_args)
