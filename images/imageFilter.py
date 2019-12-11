import cv2
import os, logging

LOG_FORMAT = "%(process)d: %(asctime)s————%(levelname)s————%(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

width = 50
height = 100
imgPath = 'K:/1aaaaa/hat_sum/images'


def ifImageAvailable(imgFile, width, height):
    print(imgFile)
    img = cv2.imread(imgFile)
    logging.log(logging.INFO, str(img.shape))


if __name__ == '__main__':
    img=cv2.imread('K:/1aaaaa/hat_sum/images/1_0.jpg')
    logging.info(img)
    # for root,dir,files in os.walk(imgPath):
    #     print(root,dir,files)
    # for image in files:
    #     logging.log(logging.INFO,root+image)
    #     ifImageAvailable(root+image,width,height)
    for image in os.listdir(imgPath):
        path=os.path.join(imgPath,image)
        print(path)
        logging.log(logging.INFO,path)
        ifImageAvailable(os.path.join(imgPath,image),width,height)
