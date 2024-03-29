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
    import argparse

    parser = argparse.ArgumentParser(description="Generate png files")
    parser.add_argument(
        "-id", "--input_dir", dest="input_directory",
        help="input path to a JPG files and output path by default "
    )
    parser.add_argument(
        "-od", "--output_dir", dest="output_directory", default=None,
        help="another path to a resized (changed)  PNG files"
    )
    args = parser.parse_args()
    new_shape = (512, 512)
    input_dir = args.input_directory
    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory

    output_image_path = output_dir + "/images"
    output_mask_path = output_dir + "/masks"
    pathlib.Path(output_image_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(output_mask_path).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']
    count = 0
    for file in files:
        # print(file)
        file_name, ext = file.split('.')
        if ext == 'png':
            print('{}{}.png'.format(input_dir, file_name))

            im1 = cv2.imread('{}{}'.format(input_dir, file), cv2.IMREAD_UNCHANGED)
            im1 = cv2.resize(im1, new_shape)
            cv2.imwrite('{}{}.jpg'.format(output_image_path, file_name), im1)
            # im1 = resize_and_cut(im1)
            im2 = image_to_mask(im1)

            cv2.imwrite('{}{}_label.png'.format(output_mask_path, file_name), im2)
