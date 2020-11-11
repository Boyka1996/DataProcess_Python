import argparse
import logging
import os
import shutil

import cv2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='......%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def parse_args():
    parser = argparse.ArgumentParser(description='End-to-end inference')
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
        '--tar',
        dest='tar_img',
        help='The location of xmls',
        default='/home/wzp/WZ2zp/mmdetection/tests/VOC2028/imgcut',
        type=str
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if not os.path.exists(args.tar):
        os.mkdir(args.tar)
    count = 0
    for src_xml in os.listdir(args.src_xml):
        tar_img_folder = os.path.join(args.tar, str(int(count / 5000)) + '_image')
        tar_xml_folder = os.path.join(args.tar, str(int(count / 5000)) + '_xml')
        if not os.path.exists(tar_img_folder):
            os.mkdir(tar_img_folder)
        if not os.path.exists(tar_xml_folder):
            os.mkdir(tar_xml_folder)
        src_img = os.path.join(args.src_img, src_xml.replace('.xml', '.jpg'))
        if not os.path.exists(src_img):
            continue
        cv_img = cv2.imread(src_img)
        if cv_img.shape[0] > 50 or cv_img.shape[1] > 50:
            count+=1
            shutil.copyfile(src_img, os.path.join(tar_img_folder, src_img.replace('.xml', '.jpg')))
            shutil.copyfile(os.path.join(args.src_xml, src_xml), os.path.join(tar_xml_folder, src_xml))
