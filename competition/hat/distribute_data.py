#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2020/12/8 0:15
@Author     : Boyka
@Contact    : upcvagen@163.com
@File       : distribute_data.py
@Project    : DataProcess_Python
@Description:
"""
import shutil
import os

if __name__ == '__main__':
    src_img_path = "E:/Dataset/鲁能安全管控数据集/safety_helmet/safety_helmet/images/"
    src_ann_path = "E:/Dataset/鲁能安全管控数据集/safety_helmet/safety_helmet/json/"
    tar_path = "E:/Dataset/鲁能安全管控数据集/安全帽20201208/"
    tar_train_img = os.path.join(tar_path, "train", "image")
    tar_train_ann = os.path.join(tar_path, "train", "annotation")
    tar_test_img = os.path.join(tar_path, "test", "image")
    tar_test_ann = os.path.join(tar_path, "test", "annotation")
    for folder in [tar_train_img, tar_train_ann, tar_test_img, tar_test_ann]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    count = 0
    for image in os.listdir(src_img_path):
        src_image_path = os.path.join(src_img_path, image)
        src_annotation_path = os.path.join(src_ann_path, image.replace('.jpg', '.json'))
        if os.path.exists(src_annotation_path):
            count += 1
            if count % 6 != 0:
                shutil.copyfile(src_image_path, os.path.join(tar_train_img, image))
                shutil.copyfile(src_annotation_path, os.path.join(tar_train_ann, image.replace('.jpg', '.json')))
            else:
                shutil.copyfile(src_image_path, os.path.join(tar_test_img, image))
                shutil.copyfile(src_annotation_path, os.path.join(tar_test_ann, image.replace('.jpg', '.json')))
        print(count)
