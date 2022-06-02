import cv2
import numpy as np

from cv2_imshow import cv2_imshow


def resize_rgba(imga):
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
    new_image = cv2.resize(new_image, (800, 800))
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



def add_alpha_channel_5(image):
    """
    for yandex\картошка
    :param image:
    :return:
    """
    b_channel, g_channel, r_channel = cv2.split(image)
    ##################################################
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    # cv2_imshow(s_channel, 's_channel')
    # s_channel_blurred = cv2.blur(s_channel, (10, 10))
    # cv2_imshow(s_channel_blurred, 's_channel_blurred')
    mask = cv2.threshold(s_channel, 56, 255, cv2.THRESH_BINARY)[1]
    new_mask = get_mask(mask)
    # cv2_imshow(mask, 'mask')
    image_rgba = cv2.merge((b_channel, g_channel, r_channel, new_mask))
    return resize_rgba(image_rgba)


if __name__ == '__main__':
    # image_path = r'Y:\UTILZ\MaskRCNN\potato\store\sick\bad_potato\DSC_0098.JPG'
    # img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    pictures = ['20220418_131151.jpg', '20220418_140554.jpg', '20220418_140748.jpg', '20220503_131918.jpg', '20220503_141519.jpg']
    image_path_root = r"Y:\UTILZ\MaskRCNN\potato\store\in\set31\{}"
    for picture in pictures:
        image_path = image_path_root.format(picture)
        img = cv2.imdecode(np.fromfile(image_path, np.uint8), cv2.IMREAD_UNCHANGED)
        # cv2_imshow(img, 'img')
        rgba = add_alpha_channel_5(img)
        cv2_imshow(rgba, 'rgba 1')
        # rgba = resize_rgba(rgba)
        # cv2_imshow(rgba, 'rgba 2')
        cv2.destroyAllWindows()
