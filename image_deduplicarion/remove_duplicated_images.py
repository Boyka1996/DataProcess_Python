import os
import argparse
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_args():
    """get the requisite parameters"""
    # Create resolve objects
    parser = argparse.ArgumentParser()
    # Add the requisite attributes to the parser
    parser.add_argument('--duplicates_list_path', dest='duplicates_list_path', help='path of duplicated images',
                        default='F:/数据集/鲁能安全管控/安全帽数据集/hat_datasets/duplicate_images.xlsx', type=str)
    parser.add_argument('--images_path', dest='images_path', help='path of the duplicated images folder',
                        default='F:/数据集/鲁能安全管控/安全帽数据集/hat_datasets/filtered_images', type=str)
    args = parser.parse_args()
    return args


def delete_operation(image_path, list_path):
    """Delete the redundant images from the image folder
    Notice that the operation is irreversible, please back up the original images"""
    image_list = pd.read_excel(list_path)
    logger.info(image_list.shape)
    confirmed_image = []
    for image_id, row in image_list.iterrows():
        confirmed_image.append(row[0])
        logger.info('image_id: ' + str(image_id))
        for sub_id, image_name in enumerate(row):
            if sub_id is not 0 and image_name not in confirmed_image and not pd.isnull(image_name) and os.path.exists(
                    os.path.join(image_path, image_name)):
                logger.info('Deleting image: ' + image_name)
                try:
                    os.remove(os.path.join(image_path, image_name))
                except:
                    continue


if __name__ == '__main__':
    path_args = parse_args()
    delete_operation(path_args.images_path, path_args.duplicates_list_path)
