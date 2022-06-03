import cv2
import numpy as np

from cv2_imshow import cv2_imshow
from utils.utils import get_mask, resize_rgba


def add_alpha_channel_5(image):
    """
    for yandex\картошка
    :param image:
    :return:
    """
    b_channel, g_channel, r_channel = cv2.split(image)
    ##################################################
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    # cv2_imshow(s_channel, 's_channel')
    # s_channel_blurred = cv2.blur(s_channel, (10, 10))
    # cv2_imshow(s_channel_blurred, 's_channel_blurred')
    mask = cv2.threshold(s_channel, 56, 255, cv2.THRESH_BINARY)[1]
    new_mask = get_mask(mask)
    # cv2_imshow(mask, 'mask')
    image_rgba = cv2.merge((b_channel, g_channel, r_channel, new_mask))
    return resize_rgba(image_rgba)


if __name__ == '__main__':
    # image_path = r'Y:\UTILZ\MaskRCNN\potato\store\sick\bad_potato\DSC_0098.JPG'
    # img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    pictures = ['20220418_131151.jpg', '20220418_140554.jpg', '20220418_140748.jpg', '20220503_131918.jpg', '20220503_141519.jpg']
    image_path_root = r"Y:\UTILZ\MaskRCNN\potato\store\in\set31\{}"
    for picture in pictures:
        image_path = image_path_root.format(picture)
        img = cv2.imdecode(np.fromfile(image_path, np.uint8), cv2.IMREAD_UNCHANGED)
        # cv2_imshow(img, 'img')
        rgba = add_alpha_channel_5(img)
        cv2_imshow(rgba, 'rgba 1')
        # rgba = resize_rgba(rgba)
        # cv2_imshow(rgba, 'rgba 2')
        cv2.destroyAllWindows()
