import pathlib
from os import listdir
from os.path import isfile, join

import cv2
from tqdm import tqdm

# from utils.cv2_imshow import cv2_imshow
from utils.utils import resize_rgba

def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)

def rgba_to_rgba(image, shape):
    """
    for
    :param kernel_blur:
    :param threshold:
    :param shape:
    :type shape:
    :param image:
    :return:
    """
    b_channel, g_channel, r_channel, a_channel = cv2.split(image)
    ##################################################
    image_rgba = cv2.merge((b_channel, g_channel, r_channel, a_channel))
    return resize_rgba(image_rgba, shape)

if __name__ == '__main__':
    # image_path = r'F:\VMWARE\FOLDER\UTILZ\MaskRCNN\potato\dataset\raw\train\strong5\DSC_0002.png'
    # image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    # img = rgba_to_rgba(image, (128,128), 50)
    # cv2_imshow(img)
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
        "-u", "--suffix", default=None, type=str,
        help="Suffix for name of file"
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
        # im1 = resize_and_cut(im1)

        im2 = rgba_to_rgba(im1, new_shape)
        # im2 = add_alpha_channel_2(im1, new_shape, threshold)
        if suffix is None:
            cv2.imwrite('{}.png'.format(join(output_dir, file_name)), im2)
        else:
            cv2.imwrite('{}_{}.png'.format(join(output_dir, file_name), suffix), im2)
