import pathlib
from os import listdir
from os.path import isfile, join

import cv2

# from utils.cv2_imshow import cv2_imshow

from tqdm import tqdm

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
    input_dir = args.input_directory

    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']

    in_dir = "{}/{}"

    i = 0
    for file in tqdm(files):
        image_path = in_dir.format(input_dir, file)
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image_new = image.copy()
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(image)

        # cv2_imshow(image[:,:,::-1], title='image')
        for i, v0 in enumerate(v):
            # print(v0)
            for j, v1 in  enumerate(v0):
                # print(v1)
                if v1 <= 22:
                    # print(f'h={h[i][j]}, s={s[i][j]}, v={v1}')
                    image_new[i][j][0] = 255
                    image_new[i][j][1] = 255
                    image_new[i][j][2] = 255
        # cv2_imshow(image_new[:,:,::-1], title='image_new')
        cv2.imwrite(in_dir.format(output_dir, file), image_new)