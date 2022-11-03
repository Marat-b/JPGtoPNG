import pathlib
import shutil
from os import listdir
from os.path import isfile, join
from random import randrange

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
    parser.add_argument(
        "-c", "--count", dest="count", default=10, type=int,
        help="Count items"
    )

    args = parser.parse_args()
    input_dir = args.input_directory
    count = args.count
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
        if i > count:
            i = 0
            shutil.move(in_dir.format(input_dir, file), output_dir)
            # print(in_dir.format(input_dir, file))
        i = i + 1 # + randrange(2)