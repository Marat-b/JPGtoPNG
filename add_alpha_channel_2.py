import cv2

from utils.cv2_imshow import cv2_imshow
from utils.utils import get_mask, resize_rgba


def add_alpha_channel_2(image, shape, threshold: int=100):
    """
    for set19
    :param shape:
    :param threshold:
    :param image:
    :return:
    """
    b_channel, g_channel, r_channel = cv2.split(image)
    # cv2_imshow(b_channel, 'b_channel')
    # b_channel_blurred = cv2.GaussianBlur(b_channel, (19, 19), 13, 13)
    # b_channel_blurred = cv2.blur(b_channel, (35, 35))
    # cv2_imshow(b_channel_blurred, 'b_channel_blurred')
    # b_mask = cv2.threshold(b_channel_blurred, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2_imshow(b_mask, 'b_mask')
    ##################################################
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    # cv2_imshow(h_channel, 'h_channel')
    # cv2_imshow(s_channel, 's_channel')
    h_channel_blurred = cv2.GaussianBlur(h_channel, (19, 19), 13, 13)
    # cv2_imshow(h_channel_blurred, 'h_channel_blurred')
    mask = cv2.threshold(h_channel_blurred, threshold, 255, cv2.THRESH_BINARY_INV)[1]
    new_mask = get_mask(mask)
    # cv2_imshow(mask, 'mask')
    # cv2_imshow(new_mask, 'new_mask')
    # mask_bright = cv2.threshold(h_channel_blurred, 115, 255, cv2.THRESH_BINARY)[1]
    # cv2_imshow(mask_bright, 'mask_bright')
    # kernel = np.ones((2, 2), 'uint8')
    # erode_mask = cv2.erode(mask, kernel, cv2.BORDER_REFLECT, iterations=2)
    # dilate_mask = cv2.dilate(erode_mask, kernel, cv2.BORDER_REFLECT, iterations=3)
    image_rgba = cv2.merge((b_channel, g_channel, r_channel, new_mask))
    return resize_rgba(image_rgba, shape)


if __name__ == '__main__':
    image_path = r'Y:\UTILZ\MaskRCNN\potato\dataset\raw\train\strong6\DSC_0510.JPG'
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    cv2_imshow(img, 'img')
    im = add_alpha_channel_2(img, (512, 512), 33)
    cv2_imshow(im, 'im')
