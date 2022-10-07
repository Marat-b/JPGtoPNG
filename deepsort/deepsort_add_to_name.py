import pathlib
import shutil
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
        help="another path to a resized (changed)  PNG files"
    )
    parser.add_argument(
        "-u", "--suffix", default=None, type=str,
        help="Suffix for name of file"
    )
    args = parser.parse_args()
    input_dir = args.input_directory
    suffix = args.suffix
    if args.output_directory is None:
        output_dir = args.input_directory
    else:
        output_dir = args.output_directory

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and
             join(input_dir, f).split('.')[1] != 'db']
    count = 0
    for i, file in enumerate(tqdm(files)):
        file_name, ext = file.split('.')
        shutil.copyfile(join(input_dir,file), join(output_dir,f'{file_name}{suffix}.{ext}'))