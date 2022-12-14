import cv2
import numpy as np

W = 1088
H = 608
XC = W // 2
YC = H // 2

def fairmot_resize(image):
    height, width, channels = image.shape
    # print(f'height={height}, width={width}')
    new_image = np.zeros((H, W, channels), dtype=np.uint8)
    # cv2_imshow(image, 'image')
    # cv2_imshow(new_image,'new_image')
    xc = width // 2
    yc = height // 2
    dx = XC - xc
    dy = YC - yc
    # print(f'xc={xc}, yc={yc}')
    # print(f'dx={dx}, dy={dy}')

    new_image[dy:height+dy, dx:width + dx] = image
    # print(new_image.shape)
    # cv2_imshow(new_image[:, :],'new_image')
    return new_image