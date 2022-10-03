from os import listdir
from os.path import join, isfile
import cv2

from tqdm import tqdm

from alpha_channel.add_alpha_channel6 import add_alpha_channel6
from alpha_channel.add_alpha_channel_5 import add_alpha_channel_5


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
        "-s", "--shape", default=(128, 128), type=tuple_type,
        help="New shape of image"
    )
    parser.add_argument(
        "-t", "--threshold", default=50, type=int,
        help="Threshold for image"
        )
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

    # pathlib.Path(f'{output_dir}/images').mkdir(parents=True, exist_ok=True)
    # pathlib.Path(f'{output_dir}/labels').mkdir(parents=True, exist_ok=True)

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

        if suffix is None:
            cv2.imwrite('{}.jpg'.format(join(output_dir, file_name)), im3)
        else:
            cv2.imwrite('{}_{}.jpg'.format(join(output_dir, file_name), suffix), im3)
