import os
from os import listdir
from os.path import join, isfile
import cv2
import pathlib
import shutil

from tqdm import tqdm

from add_alpha_channel6 import add_alpha_channel6
from add_alpha_channel_5 import add_alpha_channel_5


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
    output = '{:.6f} {:.6f} {:.6f} {:.6f}'.format((x+w)/(2*width), (y+height)/(2*height), w/width, h/height)
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
        "-u", "--suffix", default=None, type=str,
        help="Suffix for name of file"
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
    suffix = args.suffix


    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory

    pathlib.Path(f'{output_dir}/images/train').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'{output_dir}/labels_with_ids/train').mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']
    count = 0
    for i, file in enumerate(tqdm(files)):
        # print(file)
        file_name, ext = file.split('.')
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

        if suffix is None:
            cv2.imwrite('{}.jpg'.format(join(f'{output_dir}/images/train', file_name)), im3)
            with open(join(f'{output_dir}/labels_with_ids/train', f'{file_name}.txt'), 'w') as f:
                f.write(f'0 {i} {datas}')
        else:
            cv2.imwrite('{}_{}.jpg'.format(join(f'{output_dir}/images/train', file_name), suffix), im3)
            with open(join(f'{output_dir}/labels_with_ids/train', f'{file_name}_{suffix}.txt'), 'w') as f:
                f.write(f'0 {i} {datas}')