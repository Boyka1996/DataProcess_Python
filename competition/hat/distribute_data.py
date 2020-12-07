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
    src_img_path = ""
    tar_path = ""
    tar_train_img = os.path.join(tar_path, "train", "image")
    tar_train_ann = os.path.join(tar_path, "train", "annotation")
    tar_test_img = os.path.join(tar_path, "test", "image")
    tar_test_ann = os.path.join(tar_path, "test", "annotation")
    for path in [tar_train_img, tar_train_ann, tar_test_img, tar_test_ann]:
        os.mkdir(path)
