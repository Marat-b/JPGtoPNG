import cv2
import numpy as np

from utils.utils import get_mask

windowName = "Scale threshold"
trackbarValue = "Threshold"
blurValue = "Blur"
maxScaleUp = 255
scaleFactor = 1
scale_blur = 1


def scale_rgb(*args):
    global scaleFactor
    global scale_blur

    scaleFactor = cv2.getTrackbarPos("Threshold", "Scale threshold")
    scale_blur = cv2.getTrackbarPos("Blur", "Scale threshold")
    b_channel, g_channel, r_channel = cv2.split(image)
    b_channel_blurred = cv2.blur(b_channel, (scale_blur, scale_blur))
    mask = cv2.threshold(b_channel_blurred, scaleFactor, maxScaleUp, cv2.THRESH_BINARY_INV)[1]
    if mask is not None:
        image_masked = cv2.bitwise_and(image, image, mask=mask)
    image_masked = cv2.resize(image_masked, (800, 800))
    cv2.imshow(windowName, image_masked)


def scale_hsv(*args):
    global scaleFactor
    global scale_blur

    scaleFactor = cv2.getTrackbarPos("Threshold", "Scale threshold")
    scale_blur = cv2.getTrackbarPos("Blur", "Scale threshold")
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # b_channel, g_channel, r_channel = cv2.split(image)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    s_channel_blurred = cv2.blur(s_channel, (scale_blur, scale_blur))
    mask = cv2.threshold(s_channel_blurred, scaleFactor, maxScaleUp, cv2.THRESH_BINARY)[1]
    if mask is not None:
        image_masked = cv2.bitwise_and(image, image, mask=mask)
    # mask = cv2.resize(mask, (600, 600))
    # print(f'scaleFactor={scaleFactor}, scale_blur={scale_blur}')
    image_masked = cv2.resize(image_masked, (800, 800))
    cv2.imshow(windowName, image_masked)


def scale_hsv_by_h(*args):
    global scaleFactor
    global scale_blur

    # scaleFactor = args[0]
    scaleFactor = cv2.getTrackbarPos("Threshold", "Scale threshold")
    scale_blur = cv2.getTrackbarPos("Blur", "Scale threshold")
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    h_channel_blurred = cv2.blur(h_channel, (scale_blur, scale_blur))
    mask = cv2.threshold(h_channel_blurred, scaleFactor, maxScaleUp, cv2.THRESH_BINARY_INV)[1]
    mask = cv2.resize(mask, (600, 600))
    # print(f'scaleFactor={scaleFactor}, scale_blur={scale_blur}')
    cv2.imshow(windowName, mask)


cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)

# load an image
# image_path = r"Y:\UTILZ\MaskRCNN\potato\store\in\set32\20220513_144430.jpg"
# image_path = r"F:\VMWARE\FOLDER\UTILZ\MaskRCNN\potato\dataset\raw\validate\internalrot\t\20220624_182509.jpg"
# image_path = r"Y:\UTILZ\MaskRCNN\potato\dataset\raw\train\necrosis\20220529_135716.jpg"
image_path = r"F:\VMWARE\FOLDER\UTILZ\MaskRCNN\potato\dataset\raw\train\bad20220829\DSC_0646.JPG"
# image_path = r"Y:\UTILZ\MaskRCNN\potato\dataset\raw\train\alternariosis\20220603_140711.jpg"
# image_path = r"Y:\UTILZ\MaskRCNN\potato\dataset\raw\train\fusarium20220809\t\20220807_181635.jpg"
# image_path = r"Y:\UTILZ\MaskRCNN\potato\dataset\raw\train\phytophthorosis\20220601_152635.jpg"
# image_path = r"Y:\UTILZ\MaskRCNN\potato\dataset\raw\train\pinkrot\20220528_171637.jpg"
# image_path = r"Y:\UTILZ\MaskRCNN\potato\dataset\raw\train\scab20220809\t\20220727_132839.jpg"
image = cv2.imdecode(np.fromfile(image_path, np.uint8), cv2.IMREAD_UNCHANGED)
# cv2.createTrackbar(trackbarValue, windowName, scaleFactor, 255, scale_hsv)
# cv2.createTrackbar(blurValue, windowName, scale_blur, 100, scale_hsv)
cv2.createTrackbar(trackbarValue, windowName, scaleFactor, 255, scale_rgb)
cv2.createTrackbar(blurValue, windowName, scale_blur, 100, scale_rgb)

# Create a window to display results

# scale_hsv(2)

while True:
    c = cv2.waitKey(20)
    if c == 27:
        break

cv2.destroyAllWindows()
