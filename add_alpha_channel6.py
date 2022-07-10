import cv2

from utils.utils import get_mask, resize_rgba


def add_alpha_channel6(image, shape, threshold: int, kernel_blur: int = 1):
    b_channel, g_channel, r_channel = cv2.split(image)
    b_channel_blurred = cv2.blur(b_channel, (kernel_blur, kernel_blur))
    mask = cv2.threshold(b_channel_blurred, threshold, 255, cv2.THRESH_BINARY_INV)[1]
    new_mask = get_mask(mask)
    image_rgba = cv2.merge((b_channel, g_channel, r_channel, new_mask))
    return resize_rgba(image_rgba, shape)
