import os
from os import listdir
from os.path import isfile, join

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
        help="ath of output files"
    )

    args = parser.parse_args()
    input_dir = args.input_directory
    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']

    with open(join(output_dir, "list_files.txt"), 'w') as f:
        for i, file in enumerate(tqdm(files)):
                f.write(f'{os.path.join(input_dir, file)}\n')