import cv2

from utils.cv2_imshow import cv2_imshow


def add_alpha_channel_4(image):
    b_channel, g_channel, r_channel = cv2.split(image)
    cv2_imshow(b_channel, 'b_channel')
    cv2_imshow(g_channel, 'g_channel')
    cv2_imshow(r_channel, 'r_channel')
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    cv2_imshow(h_channel, 'h_channel')
    cv2_imshow(s_channel, 's_channel')
    cv2_imshow(v_channel, 'v_channel')


if __name__ == '__main__':
    image_path = r'Y:\UTILZ\MaskRCNN\potato\store\sick\bad_potato\DSC_0415.JPG'
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    cv2_imshow(img, 'img')
    add_alpha_channel_4(img)
    # cv2_imshow(im, 'im')
