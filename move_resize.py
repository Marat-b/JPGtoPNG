from os import listdir
from os.path import join, isfile
import cv2
import pathlib

from tqdm import tqdm

from add_alpha_channel_2 import add_alpha_channel_2
from add_alpha_channel_5 import add_alpha_channel_5


def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)


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
        "-u", "--suffix", default='z', type=str,
        help="New shape of image"
    )

    args = parser.parse_args()
    input_dir = args.input_directory
    new_shape = args.shape
    suffix = args.suffix
    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']
    count = 0
    for file in tqdm(files):
        # print(file)
        file_name, ext = file.split('.')
        # print('{}.png'.format(join(input_dir, file_name)))

        im1 = cv2.imread(join(input_dir, file), cv2.IMREAD_UNCHANGED)
        im2 = cv2.resize(im1, new_shape)
        new_file_name = '{}_{}.{}'.format(file_name, suffix, ext)
        cv2.imwrite(join(output_dir, new_file_name), im2)
