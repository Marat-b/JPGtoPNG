import os
from os import listdir
from os.path import join, isfile
import cv2
import pathlib

from tqdm import tqdm

from utils.utils import get_mask, resize_rgba, rgba2mask

def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)

if __name__ == '__main__':
    # for deeplabv3
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
    args = parser.parse_args()
    new_shape = args.shape
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
    number_of_files = len(os.listdir(output_image_path))
    count = 0
    for i, file in enumerate(tqdm(files)):
        # print(file)
        file_name, ext = file.split('.')
        if ext == 'png':
            j =  i + number_of_files
            # print('{}/{}.png'.format(input_dir, file_name))

            im1 = cv2.imread('{}/{}'.format(input_dir, file), cv2.IMREAD_UNCHANGED)
            im1 = cv2.resize(im1, new_shape)
            im2, mask = rgba2mask(im1)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            if im2 is not None:
                cv2.imwrite('{}/potato{}.jpg'.format(output_image_path, str(j)), im2)
                cv2.imwrite('{}/mask{}.png'.format(output_mask_path, str(j)), mask)
