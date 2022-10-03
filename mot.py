import os
from os import listdir
from os.path import join, isfile
import cv2
import pathlib

from tqdm import tqdm

from alpha_channel.add_alpha_channel6 import add_alpha_channel6
from alpha_channel.add_alpha_channel_5 import add_alpha_channel_5


def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)


def get_sizes(image):
    maxArea = 0
    ind = 0
    # image = imga[:, :, 3].copy()
    # img = imga[:, :, :-1]
    height, width = image.shape
    # print(image.shape)
    # cv2_imshow(image, 'image')

    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print("Number of contours found = %2d" % len(contours))

    for index, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if maxArea < area:
            maxArea = area
            ind = index

    cnt = contours[ind]
    # delta = 50  # 50 pixels out of border
    x, y, w, h = cv2.boundingRect(cnt)
    # print(f'x={x}, y={y}, w={w}, h={h}')
    output = '{:d},{:d},{:d},{:d},1,1,1'.format(x, y, w, h)
    # print(output)
    return output


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
    parser.add_argument(
        "-s", "--shape", default=(512, 512), type=tuple_type,
        help="New shape of image"
    )
    parser.add_argument(
        "-t", "--threshold", default=50, type=int,
        help="Threshold for image"
        )
    parser.add_argument(
        "-k", "--kernel", default=1, type=int,
        help="Kernel of blur"
    )
    parser.add_argument(
        "-rgb", "--rgb_mask", default=False, type=bool,
        help="RGB mask is choose"
    )

    args = parser.parse_args()
    input_dir = args.input_directory
    kernel = args.kernel
    new_shape = args.shape
    rgb_mask = args.rgb_mask
    threshold = args.threshold

    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory

    img_dir = f'{output_dir}/img1'
    gt_dir = f'{output_dir}/gt'
    pathlib.Path(img_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(gt_dir).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']
    number_of_files = len(os.listdir(img_dir))
    gt = []
    for i, file in enumerate(tqdm(files)):
        # print(file)
        j = 1 + i + number_of_files
        # print('{}.png'.format(join(input_dir, file_name)))

        im1 = cv2.imread(join(input_dir, file), cv2.IMREAD_UNCHANGED)
        # im1 = resize_and_cut(im1)
        if rgb_mask:
            # RGB channels
            im2 = add_alpha_channel6(im1, new_shape, threshold, kernel)
        else:
            # HSV channels
            im2 = add_alpha_channel_5(im1, new_shape, threshold, kernel)
        # im2 = add_alpha_channel_2(im1, new_shape, threshold)
        im3 = im2[:, :, :-1]
        datas = get_sizes(im2[:, :, 3])

        cv2.imwrite('{}.jpg'.format(join(img_dir, str(j).rjust(6, '0'))), im3)
        gt.append(f'{j},1,{datas}')
    with open(join(gt_dir, 'gt.txt'), 'a') as f:
        for g in gt:
            f.write(f'{g}\n')

    print(f'Count={j}\nNext number={j + 1}')
