import os
import sys
from os import listdir
from os.path import join, isfile
import cv2
import pathlib

from tqdm import tqdm

# sys.path.append('../utils')
from fairmot_resize import fairmot_resize

sys.path.append('..')
from alpha_channel.add_alpha_channel6 import add_alpha_channel6
from alpha_channel.add_alpha_channel_5 import add_alpha_channel_5
from utils.utils import resize_rgba

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
    output = '{:.6f} {:.6f} {:.6f} {:.6f}'.format((x+w/2)/width, (y+h/2)/height, w/width, h/height)
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
    parser.add_argument("-t", "--threshold", default=50, type=int,
                        help="Threshold for image")
    parser.add_argument(
        "-k", "--kernel", default=1, type=int,
        help="Kernel of blur"
    )
    parser.add_argument(
        "-rgb", "--rgb_mask", default=False, action="store_true",
        help="RGB mask is choose"
    )
    parser.add_argument(
        "-sn", "--start_number", default=0, type=int,
        help="Start number"
    )
    parser.add_argument(
        "-m", "--use_mask", action='store_true', default=False,
        help="Using only file mask"
    )
    parser.add_argument(
        "-c", "--count", dest="count", default=10, type=int,
        help="Count items"
    )

    args = parser.parse_args()
    input_dir = args.input_directory
    kernel = args.kernel
    new_shape = args.shape
    rgb_mask = args.rgb_mask
    threshold = args.threshold
    start_number = args.start_number
    use_mask = args.use_mask
    count_items = args.count

    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory

    img_dir = f'{output_dir}/images/train'
    labels_dir = f'{output_dir}/labels_with_ids/train'
    pathlib.Path(img_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(labels_dir).mkdir(parents=True, exist_ok=True)
    img_dir_val = f'{output_dir}/images/val'
    labels_dir_val = f'{output_dir}/labels_with_ids/val'
    pathlib.Path(img_dir_val).mkdir(parents=True, exist_ok=True)
    pathlib.Path(labels_dir_val).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']
    count = 0
    number_of_files = len(os.listdir(img_dir)) + len(os.listdir(img_dir_val))
    for i, file in enumerate(tqdm(files)):
        # print(file)
        j = 1 + i + number_of_files + start_number
        file_name, ext = file.split('.')
        # print('{}.png'.format(join(input_dir, file_name)))

        im1 = cv2.imread(join(input_dir, file), cv2.IMREAD_UNCHANGED)
        # im1 = resize_and_cut(im1)
        if use_mask:
            im2 =resize_rgba(im1, new_shape)
        else:
            if rgb_mask:
                # RGB channels
                im2 = add_alpha_channel6(im1, new_shape, threshold, kernel)
            else:
                # HSV channels
                im2 = add_alpha_channel_5(im1, new_shape, threshold, kernel)
        # im2 = add_alpha_channel_2(im1, new_shape, threshold)
        im2 = fairmot_resize(im2)
        im3 = im2[:, :, :-1]
        datas = get_sizes(im2[:, :, 3])

        if j % count_items == 0:
            cv2.imwrite('{}.jpg'.format(join(img_dir_val, str(j).rjust(6, '0'))), im3)
            with open(join(labels_dir_val, f"{str(j).rjust(6, '0')}.txt"), 'w') as f:
                f.write(f'0 {j} {datas}')
        else:
            cv2.imwrite('{}.jpg'.format(join(img_dir, str(j).rjust(6, '0'))), im3)
            with open(join(labels_dir, f"{str(j).rjust(6, '0')}.txt"), 'w') as f:
                f.write(f'0 {j} {datas}')


    print(f'Count={j}')