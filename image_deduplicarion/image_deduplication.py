from imagededup.methods import PHash
from xlwt import *
import os

if __name__ == '__main__':
    phasher = PHash()
    file = Workbook(encoding='utf-8')
    table = file.add_sheet('data')
    # 生成图像目录中所有图像的二值hash编码
    encodings = phasher.encode_images(image_dir=r'F:/数据集/鲁能安全管控/安全帽数据集/hat_datasets/filtered_images')

    # 对已编码图像寻找重复图像
    duplicates = phasher.find_duplicates(encoding_map=encodings)
    print('=' * 20)
    print(duplicates)
    print(type(duplicates))
    print('=' * 20)
    count = 0
    for key in duplicates:
        if len(duplicates[key]) is not 0:
            table.write(count, 0, key)
            for image_id, image in enumerate(duplicates[key]):
                table.write(count, image_id + 1, image)
            count += 1
    if os.path.exists('duplicate_images.xlsx'):
        # os.remove('duplicate_images.xlsx')
        file.save('duplicate_images1.xlsx')
    else:
        file.save('duplicate_images.xlsx')
    # # 给定一幅图像，显示与其重复的图像
    # from imagededup.utils import plot_duplicates
    #
    # plot_duplicates(image_dir=r'E:/PycharmProjects/DataProcess_Python/files',
    #                 duplicate_map=duplicates,
    #                 filename='7c1ec0729e62c65e2a70bfa4a02e6380.jpg')
