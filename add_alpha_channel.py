import cv2
import numpy as np
import matplotlib.pyplot as plt


def add_alpha_channel(image):
    # print(image)
    b_channel, g_channel, r_channel = cv2.split(image)
    # cv2.imshow('b_channel', b_channel)
    # cv2.imshow('r_channel', r_channel)

    thresh, mask = cv2.threshold(b_channel, 220, 255, cv2.THRESH_BINARY_INV)
    # print(mask)
    # cv2.imshow('mask', mask)
    # masked_image = cv2.bitwise_and(image, image, mask=mask)
    # cv2.imshow('masked_image', masked_image)

    # alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 0
    # cv2.imshow('alpha_channel', alpha_channel)
    # b_channel, g_channel, r_channel = cv2.split(masked_image)
    image_rgba = cv2.merge((b_channel, g_channel, r_channel, mask))
    # image_rgba = np.dstack((masked_image, alpha_channel))
    # cv2.imshow('image_rgba', image_rgba)
    # print(image_rgba.shape)
    return image_rgba


# def add_alpha_channel_2(image):
#     """
#     for set19
#     :param image:
#     :return:
#     """
#     b_channel, g_channel, r_channel = cv2.split(image)
#     image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     h_channel, s_channel, v_channel = cv2.split(image_hsv)
#     s_channel_blurred = cv2.GaussianBlur(s_channel, (15, 15), 9, 9)
#     mask = cv2.threshold(s_channel_blurred, 100, 255, cv2.THRESH_BINARY)[1]
#     # kernel = np.ones((2, 2), 'uint8')
#     # erode_mask = cv2.erode(mask, kernel, cv2.BORDER_REFLECT, iterations=2)
#     # dilate_mask = cv2.dilate(erode_mask, kernel, cv2.BORDER_REFLECT, iterations=3)
#     image_rgba = cv2.merge((b_channel, g_channel, r_channel, mask))
#     return image_rgba
def add_alpha_channel_2(image):
    """
    for set19
    :param image:
    :return:
    """
    b_channel, g_channel, r_channel = cv2.split(image)
    b_channel_blurred = cv2.blur(b_channel, (35, 35))
    mask = cv2.threshold(b_channel_blurred, 100, 255, cv2.THRESH_BINARY_INV)[1]
    image_rgba = cv2.merge((b_channel, g_channel, r_channel, mask))
    return image_rgba



def add_alpha_channel_3(image):
    """
    for set26
    :param image:
    :return:
    """
    image = cv2.resize(image, (600, 402))
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    b_channel, g_channel, r_channel = cv2.split(image)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    h_channel_blurred = cv2.blur(h_channel, (35, 35))
    kernel = np.ones((12, 12), 'uint8')
    erode_mask = cv2.erode(h_channel_blurred, kernel, cv2.BORDER_REFLECT, iterations=6)
    dilate_mask = cv2.dilate(erode_mask, kernel, cv2.BORDER_REFLECT, iterations=8)
    mask = cv2.threshold(dilate_mask, 30, 255, cv2.THRESH_BINARY_INV)[1]
    ##################################################
    kernel = np.ones((14, 14), 'uint8')
    mask_bright = cv2.threshold(h_channel_blurred, 60, 255, cv2.THRESH_BINARY)[1]
    erode_mask = cv2.erode(mask_bright, kernel, cv2.BORDER_REFLECT, iterations=3)
    dilate_mask_2 = cv2.dilate(erode_mask, kernel, cv2.BORDER_REFLECT, iterations=5)
    mask_united = cv2.bitwise_or(mask, dilate_mask_2)
    ###################################################

    image_rgba = cv2.merge((b_channel, g_channel, r_channel, mask_united))
    return image_rgba


if __name__ == '__main__':
    image_path = r'Y:\UTILZ\MaskRCNN\potato\store\in\set26\DSC_0487.JPG'
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    im = add_alpha_channel_3(img)
    plt.title('im')
    # plt.imshow(im[:, :, [2, 1, 0]])
    plt.imshow(im)
    plt.show()
    # cv2.imshow('im', im)
    # cv2.imwrite('im.png', im)
    # if cv2.waitKey(50000) == 27:
    #     pass
