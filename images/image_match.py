# -*- coding: utf-8 -*-
# School                 ：UPC
# Author                 ：Boyka
# File Name              ：image_match.py
# Computer User          ：Administrator 
# Current Project        ：DataProcess_Python
# Development Time       ：2020/2/20  23:23 
# Development Tool       ：PyCharm
import cv2
import matplotlib as plt
import numpy as np


def matchAB(imgA, imgB):
    # 转换成灰色
    grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)
    result=grayA-grayB
    # result=int(grayA)-int(grayB)
    return result

    # result=int+
    print(grayA.shape)

    # 获取图片A的大小
    height, width = grayA.shape
    result=np.zeros((height, width), dtype=imgA.dtype)
    for x_id,x in enumerate(result):
        for y_id,y in enumerate(result[x_id]):
            if abs(int(grayA[x_id][y_id])-int(grayB[x_id][y_id]))<10:
                result[x_id][y_id]=255
    return result

    # # 取局部图像，寻找匹配位置
    # result_window = np.zeros((height, width), dtype=imgA.dtype)
    # for start_y in range(0, height - 100, 10):
    #     for start_x in range(0, width - 100, 10):
    #         window = grayA[start_y:start_y + 100, start_x:start_x + 100]
    #         match = cv2.matchTemplate(grayB, window, cv2.TM_CCOEFF_NORMED)
    #         _, _, _, max_loc = cv2.minMaxLoc(match)
    #         matched_window = grayB[max_loc[1]:max_loc[1] + 100, max_loc[0]:max_loc[0] + 100]
    #         result = cv2.absdiff(window, matched_window)
    #         result_window[start_y:start_y + 100, start_x:start_x + 100] = result
    # print(type(result_window))
    # return result_window


if __name__ == '__main__':
    img1=cv2.imread('1.jpg')
    img2=cv2.imread('2.jpg')
    cv2.imwrite('result1.jpg',matchAB(img1,img2))
    # gif = cv2.VideoCapture("E:/蔡徐坤.avi")
    # ret, source_img = gif.read()  # ret=True if it finds a frame else False. Since your gif contains only one frame, the next read() will give you ret=False
    #
    # count = 0
    # cv2.imwrite('1.jpg',source_img)
