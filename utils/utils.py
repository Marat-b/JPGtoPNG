import cv2
import numpy as np

from cv2_imshow import cv2_imshow


def resize_rgba(imga, shape):
    maxArea = 0
    ind = 0
    image = imga[:, :, 3].copy()
    # img = imga[:, :, :-1]
    # height, width = image.shape
    # print(image.shape)
    # cv2_imshow(image, 'image')

    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print("Number of contours found = %2d" % len(contours))

    for index, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if maxArea < area:
            maxArea = area
            ind = index

    # print(f'ind={str(ind)}')
    # imgContours = img.copy()
    # cv2.drawContours(imgContours, contours, ind, (255, 0, 0), 14, cv2.LINE_AA)
    # cv2_imshow(imgContours, 'imgContours')
    cnt = contours[ind]
    # delta = 50  # 50 pixels out of border
    x, y, w, h = cv2.boundingRect(cnt)
    # print(f'w={w}, h={h}')
    l = cv2.minAreaRect(cnt)[1]
    # print(f'l={l}')
    length = l[0] if l[0] > l[1] else l[1]
    length = length if length > w else w
    length = length if length > h else h
    # print(f'length={int(length)}')
    hd = int((length - h) / 2)
    wd = int((length - w) / 2)
    x = x - wd if x - wd >= 0 else 0
    y = y - hd if y - hd >= 0 else 0
    w = int(length)
    h = int(length)
    # cv2.rectangle(imgContours, (x, y), (x + w, y + h), (255, 0, 0), 14)
    # cv2_imshow(imgContours, 'rect')
    new_image = imga[y:y + h, x: x + w, :]
    new_image = cv2.resize(new_image, shape)
    return new_image


def get_mask(maska):
    maxArea = 0
    ind = 0
    mask = maska.copy()
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for index, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if maxArea < area:
            maxArea = area
            ind = index

    contour = contours[ind]
    # cv2_imshow(mask, 'mask')
    canvas = np.zeros_like(mask)
    # print(contour.shape, contour.dtype)
    # cv2_imshow(canvas, 'canvas')
    cv2.fillPoly(canvas, [contour], (255, 255, 255))
    # cv2_imshow(canvas, 'canvas')
    return canvas


def rgba2mask(rgba_image):
    if rgba_image.shape[2] == 4:
        image = rgba_image[:, :, :-1].copy()
        # cv2_imshow(image)
        mask = rgba_image[:, :, 3].copy()
        # cv2_imshow(mask)
        image_mask = cv2.merge((mask, mask, mask))
        # cv2_imshow(image_mask)
        return image, image_mask
    else:
        return None, None


if __name__ == '__main__':
    img = cv2.imread('../images/DSC_0630.png', cv2.IMREAD_UNCHANGED)
    cv2_imshow(img)
    rgba2mask(img)
