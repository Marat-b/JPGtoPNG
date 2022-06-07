import cv2
import numpy as np

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
    mask = cv2.threshold(b_channel_blurred, scaleFactor, maxScaleUp, cv2.THRESH_BINARY)[1]
    mask = cv2.resize(mask, (600, 600))
    cv2.imshow(windowName, mask)


def scale_hsv(*args):
    global scaleFactor
    global scale_blur

    # scaleFactor = args[0]
    scaleFactor = cv2.getTrackbarPos("Threshold", "Scale threshold")
    scale_blur = cv2.getTrackbarPos("Blur", "Scale threshold")
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    s_channel_blurred = cv2.blur(s_channel, (scale_blur, scale_blur))
    mask = cv2.threshold(s_channel_blurred, scaleFactor, maxScaleUp, cv2.THRESH_BINARY)[1]
    mask = cv2.resize(mask, (600, 600))
    print(f'scaleFactor={scaleFactor}, scale_blur={scale_blur}')
    cv2.imshow(windowName, mask)


cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)

# load an image
# image_path = r"Y:\UTILZ\MaskRCNN\potato\store\in\set32\20220513_144430.jpg"
image_path = r"C:\softz\work\potato\in\images\set37\photo_2022-06-06_15-51-19.jpg"
image = cv2.imdecode(np.fromfile(image_path, np.uint8), cv2.IMREAD_UNCHANGED)
cv2.createTrackbar(trackbarValue, windowName, scaleFactor, 255, scale_hsv)
cv2.createTrackbar(blurValue, windowName, scale_blur, 100, scale_hsv)
# Create a window to display results

# scale_hsv(2)

while True:
    c = cv2.waitKey(20)
    if c == 27:
        break

cv2.destroyAllWindows()
