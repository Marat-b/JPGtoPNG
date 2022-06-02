from os import listdir
from os.path import join, isfile
import cv2
import pathlib

from add_alpha_channel import *
from add_alpha_channel_5 import add_alpha_channel_5


def resize_and_cut(image):
    image_resized = cv2.resize(image, (600, 401))
    image_resized = image_resized[:, :550]
    return image_resized


if __name__ == '__main__':
    number = 36
    root_path = 'Y:\\UTILZ\\MaskRCNN\\potato\\'
    input_path = '{}store\\in\\set{}\\'.format(root_path, str(number))

    output_path = '{}set{}\\input\\foregrounds\\potato\\potato_sick\\'.format(root_path, str(number))
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_path) if isfile(join(input_path, f)) and
             join(input_path, f).split('.')[1] != 'db']
    count = 0
    for file in files:
        # print(file)
        file_name, ext = file.split('.')
        print('{}{}.png'.format(input_path, file_name))

        im1 = cv2.imread('{}{}'.format(input_path, file), cv2.IMREAD_UNCHANGED)
        # im1 = resize_and_cut(im1)
        im2 = add_alpha_channel_5(im1)


        cv2.imwrite('{}{}.png'.format(output_path, file_name), im2)
