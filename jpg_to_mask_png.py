from os import listdir
from os.path import join, isfile
import cv2
import pathlib

from utils.utils import get_mask, resize_rgba


def image_to_mask(image):
    """
    for yandex\картошка
    :param image:
    :return:
    """
    # b_channel, g_channel, r_channel = cv2.split(image)
    ##################################################
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    # cv2_imshow(s_channel, 's_channel')
    # s_channel_blurred = cv2.blur(s_channel, (10, 10))
    # cv2_imshow(s_channel_blurred, 's_channel_blurred')
    mask = cv2.threshold(s_channel, 56, 255, cv2.THRESH_BINARY)[1]
    new_mask = get_mask(mask)
    # cv2_imshow(mask, 'mask')
    image_rgb = cv2.merge((new_mask, new_mask, new_mask))
    return image_rgb


if __name__ == '__main__':
    number = 36
    root_path = r'C:\softz\test\python\DeepLabv3FineTuning-master\potato\\'
    input_path = '{}set{}\Images\\'.format(root_path, str(number))

    output_path = '{}set{}\\Masks\\'.format(root_path, str(number))
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_path) if isfile(join(input_path, f)) and
             join(input_path, f).split('.')[1] != 'db']
    count = 0
    for file in files:
        # print(file)
        file_name, ext = file.split('.')
        if ext == 'png':
            print('{}{}.png'.format(input_path, file_name))

            im1 = cv2.imread('{}{}'.format(input_path, file), cv2.IMREAD_UNCHANGED)
            cv2.imwrite('{}{}.jpg'.format(input_path, file_name), im1)
            # im1 = resize_and_cut(im1)
            im2 = image_to_mask(im1)

            cv2.imwrite('{}{}_label.png'.format(output_path, file_name), im2)
