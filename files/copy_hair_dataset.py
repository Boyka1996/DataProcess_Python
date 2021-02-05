import os, shutil
import logging

LOG_FORMAT = "%(process)d: %(asctime)s————%(levelname)s————%(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

srcImg = 'K:/1aaaaa/hairLabel/images'
srcXml = 'K:/1aaaaa/hairLabel/Annotations'
srcTxt = 'K:/1aaaaa/hairLabel/labels'
tarImg = 'E:/Dataset/鲁能安全管控数据集/安全帽/头发/images'
tarXml = 'E:/Dataset/鲁能安全管控数据集/安全帽/头发/xml'
tarTxt = 'E:/Dataset/鲁能安全管控数据集/安全帽/头发/txt'

if __name__ == '__main__':
    for img in os.listdir(srcImg):
        logging.info(img)
        xml = img.replace('.jpg', '.xml')
        txt = img.replace('.jpg', '.txt')
        if os.path.exists(os.path.join(srcXml, xml)):
            shutil.copyfile(os.path.join(srcXml, xml), os.path.join(tarXml, xml))
            shutil.copyfile(os.path.join(srcImg, img), os.path.join(tarImg, img))
        if os.path.exists(os.path.join(srcXml, xml)):
            shutil.copyfile(os.path.join(srcXml, xml), os.path.join(tarXml, xml))
