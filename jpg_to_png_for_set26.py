from os import listdir
from os.path import join, isfile
import cv2
import pathlib

from tqdm import tqdm

from alpha_channel.add_alpha_channel_7 import add_alpha_channel_7


def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)


def resize_and_cut(image):
    image_resized = cv2.resize(image, (600, 401))
    image_resized = image_resized[:, :550]
    return image_resized


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

    args = parser.parse_args()
    input_dir = args.input_directory
    new_shape = args.shape
    kernel = args.kernel
    threshold = args.threshold

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
        # im1 = resize_and_cut(im1)

        im2 = add_alpha_channel_7(im1, new_shape, threshold, kernel)

        cv2.imwrite('{}_26.png'.format(join(output_dir, file_name)), im2)
