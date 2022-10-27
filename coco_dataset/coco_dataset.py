import json
import os
import pathlib
from collections import defaultdict
from pathlib import Path
from typing import Callable, List, Optional

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

# from utils.cv2_imshow import cv2_imshow


class PotatoSample():
    def __init__(self, data_instances=[], new_shape=(512, 512)):
        self.cat_ids = 0
        self.count_images = 0
        self.data_instances = data_instances
        self.dataset = dict()
        self.img_segments, self.cat_ids = defaultdict(list), defaultdict(list)
        self.new_shape = new_shape
        self.sample = {'image': [], 'mask': []}
        self.sub_sample = self.sample.copy()

        self.create_dataset()

    def __getitem__(self, index):
        smpl = self.get_sample(index)
        image = smpl['image']
        mask = smpl['mask']
        return image, mask

    def __len__(self):
        # print(f'len(self.img_segments)={len(self.img_segments)}')
        return len(self.img_segments)

    def create_dataset(self):
        for data_instance in self.data_instances:
            # tic = time.time()
            self.images_path = data_instance[1]
            if Path(data_instance[0]).exists():
                # print(f'Load dataset:{data_instance[0]}')
                dataset = json.load(open(data_instance[0], 'r'))
                assert type(dataset) == dict, 'annotation file format {} not supported'.format(type(dataset))
                # print('Done (t={:0.2f}s)'.format(time.time() - tic))
                self.dataset = dataset
                self.create_index(self.images_path)
                # self.get_mask(self.sample)
            else:
                raise OSError(f"{data_instance[0]} does not exist.")
        # print('End to get instances...')

    def create_index(self, path: str) -> None:
        """
        create index from annotation's file
        :return: None
        :rtype:
        """

        def get_annotation(index: int):
            img_to_segments = []
            if 'annotations' in self.dataset:
                for ann in self.dataset['annotations']:
                    if ann['image_id'] == index:
                        img_to_segments.append(
                            {
                                'segmentation': ann['segmentation'],
                                'category_id': ann['category_id']
                            }
                        )
            return img_to_segments

        imgs = {}

        if 'images' in self.dataset:
            for img in self.dataset['images']:
                imgs[img['id']] = img

        for img in imgs.keys():
            # print(f'--> img={img}')
            self.img_segments[self.count_images].append(
                {
                    'path': path,
                    'file_name': imgs[img]['file_name'],
                    'height': imgs[img]['height'],
                    'width': imgs[img]['width'],
                    'annotations': get_annotation(imgs[img]['id'])
                }
            )
            self.count_images += 1
        if 'categories' in self.dataset:
            cat_ids = [cat['id'] for cat in self.dataset['categories']]
        # print(f'imgs={imgs}')
        # print(f'img_segments={self.img_segments}')
        # print(f'cat_ids={cat_ids}')
        # self.imgs = imgs
        # self.img_to_segments = img_to_segments
        self.cat_ids = cat_ids
        # self.cat_ids = [1]

    def get_image(self, images_path, file_name):
        if Path(os.path.join(images_path, file_name)).exists():
            image = Image.open(os.path.join(images_path, file_name))
            # image = np.asarray(self._scale(np.asarray(image), self.new_shape))
            image = np.asarray(image)
            # shape = image.shape
            # print(f'get_image image.shape={shape}')
            # image = np.transpose(image, (2, 0, 1))
            return image
        else:
            print(f' Path {os.path.join(self.images_path, file_name)} does not exists')
            return None

    def get_mask(self, img_segment):
        sample = {}
        img_segment = img_segment[0]
        # print(f'img_segment={img_segment}')
        image = self.get_image(img_segment['path'], img_segment['file_name'])
        if image is not None:
            masks = []
            # print(f'empty bitmasks.shape={bitmasks.shape}')
            for img_to_segment in img_segment['annotations']:
                masks.append(self._polygons_to_masks(image, img_to_segment['segmentation']))

            sample['image'] = img_segment['file_name']
            sample['mask'] = masks

        return sample



    def get_sample(self, index):
        img_segment = self.img_segments[index]
        # print(f'img_segment={img_segment}')
        sample = self.get_mask(img_segment)
        return sample



    def _polygons_to_masks(self, image, polygons: List[np.ndarray]) -> List[np.ndarray]:
        masks = []
        try:
            for polygon in polygons:
                points = np.array(polygon).reshape(-1,2)
                # print(f'points={points}')
                # cnt = cv2.contourArea(np.array(polygon).reshape(-1, 2)) #.T.astype(np.float32))
                x,y,w,h = cv2.boundingRect(points)  # .T.astype(np.float32))
                # print(x, y, w, h)
                new_image = image[y:y+h, x:x+w, :]
                # cv2_imshow(new_image)
                points[:, [0]] -= x
                points[:, [1]] -= y
                # print(points)
                mask = np.zeros((h, w, 1), np.uint8)
                cv2.fillPoly(mask, [points], (255, 255, 255))
                # cv2_imshow(mask, 'mask')
                # print(f'mask.shape={mask.shape}, new_image.shape={new_image.shape}')
                new_image = cv2.merge((new_image, mask))
                new_image = cv2.resize(new_image, (128, 128))
                masks.append(new_image)
                # cv2_imshow(new_image)
                # print(f'cnt={cnt}')
        except:
            pass
        return masks


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Trainer Composition")
    parser.add_argument(
        "-c", "--coco_path",
        type=str,
        dest="coco_file_path",
        required=True,
        help="Path of json file of COCO format"
    )
    parser.add_argument(
        "-i", "--images_path",
        type=str,
        dest="images_path",
        required=True,
        help="Path of image files"
    )
    parser.add_argument(
        "-o", "--output_dir", dest="output_directory", default=None,
        required=True,
        help="another path to a resized (changed)  PNG files"
    )

    args = parser.parse_args()
    coco_file_path = args.coco_file_path
    images_path = args.images_path
    output_dir = args.output_directory
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    f = os.path.split(coco_file_path)[1]
    print(f)

    samples = PotatoSample([
        (coco_file_path, images_path)],
        )
    # ps.create_dataset()
    print(f'len(samples)={len(samples)}')
    # ps.get_sample(0)
    for sample in tqdm(samples):
        file_name, masks = sample
        file_name = file_name.split('.')[0]
        # print(f'file_name={file_name}')
        for i, mask in enumerate(masks):
            for j, m in enumerate(mask):
                out_file_name = os.path.join(output_dir, f'{file_name}_{i}_{j}.png')
                # print(out_file_name)
                # cv2.imwrite(out_file_name, m)
                Image.fromarray(m).save(out_file_name)




