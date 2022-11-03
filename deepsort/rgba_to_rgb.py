from os import listdir
from os.path import join, isfile
import cv2
import pathlib

from tqdm import tqdm


if __name__ == '__main__':
    # for deepsort
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
    # new_shape = (512, 512)
    input_dir = args.input_directory
    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory

    # output_image_path = output_dir + "/images"
    # output_mask_path = output_dir + "/masks"
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # pathlib.Path(output_mask_path).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']
    # count = 0
    for file in tqdm(files):
        # print(file)
        file_name, ext = file.split('.')
        if ext == 'png':
            # print('{}/{}.png'.format(input_dir, file_name))

            im1 = cv2.imread('{}/{}'.format(input_dir, file), cv2.IMREAD_UNCHANGED)
            ##########################################################
            mask = im1[:, :, [3]] * 255
            # print(mask.shape, mask.dtype)
            image = cv2.bitwise_and(im1[:, :, :3], im1[:, :, :3],mask=mask)
            # cv2_imshow(mask, 'mask')
            # blue, green, red = cv2.split(im1[:, :, :3])
            # blue = cv2.bitwise_and(blue, blue,mask=mask)
            # green = cv2.bitwise_and(green, green, mask=mask)
            # red = cv2.bitwise_and(red, red, mask=mask)
            # image = cv2.merge((blue, green, red))
            # im1 = cv2.resize(im1, new_shape)
            # im2, mask = rgba2mask(im1)
            # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            # if im2 is not None:
            cv2.imwrite('{}/potato{}.jpg'.format(output_dir, file_name), image)
            # cv2.imwrite('{}/mask{}.png'.format(output_mask_path, str(i)), mask)
    cv2.destroyAllWindows()