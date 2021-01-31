#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/1/29 16:37
@Author     : Boyka
@Contact    : upcvagen@163.com
@File       : copy_file.py
@Project    : DataProcess_Python
@Description:
"""
import os
import shutil

src = "E:/Dataset/鲁能安全管控数据集/safety_helmet/safety_helmet"
tar = "E:/Dataset/鲁能安全管控数据集/hat/temp"
src_img = os.path.join(src, "images")
src_ann = os.path.join(src, "json")
tar_img = os.path.join(tar, "images")
tar_ann = os.path.join(tar, "Annotations")
for folder in [tar, src_img, src_ann, tar_img, tar_ann]:
    print(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
for annotation in os.listdir(src_ann):
    image = annotation.replace('.json', '.jpg')
    src_image = os.path.join(src_img, image)
    src_annotation = os.path.join(src_ann, annotation)
    tar_image = os.path.join(tar_img, image)
    tar_annotation = os.path.join(tar_ann, annotation)
    if os.path.exists(src_image) and os.path.exists(src_annotation):
        shutil.copyfile(src_image, tar_image)
        shutil.copyfile(src_annotation, tar_annotation)
