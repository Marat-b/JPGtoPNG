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
    global image
    global scaleFactor
    global scale_blur

    scaleFactor = cv2.getTrackbarPos("Threshold", "Scale threshold")
    scale_blur = cv2.getTrackbarPos("Blur", "Scale threshold")
    b_channel, g_channel, r_channel = cv2.split(image)[:3]
    b_channel_blurred = cv2.blur(b_channel, (scale_blur, scale_blur))
    mask = cv2.threshold(b_channel_blurred, scaleFactor, maxScaleUp, cv2.THRESH_BINARY_INV)[1]
    if mask is not None:
        image_masked = cv2.bitwise_and(image, image, mask=mask)
    image_masked = cv2.resize(image_masked, (800, 800))
    cv2.imshow(windowName, image_masked)


def scale_hsv(*args):
    global image
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
    global image
    global scaleFactor
    global scale_blur

    # scaleFactor = args[0]
    scaleFactor = cv2.getTrackbarPos("Threshold", "Scale threshold")
    scale_blur = cv2.getTrackbarPos("Blur", "Scale threshold")
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(image_hsv)
    h_channel_blurred = cv2.blur(h_channel, (scale_blur, scale_blur))
    mask = cv2.threshold(h_channel_blurred, scaleFactor, maxScaleUp, cv2.THRESH_BINARY_INV)[1]
    mask = cv2.resize(mask, (800, 800))
    # print(f'scaleFactor={scaleFactor}, scale_blur={scale_blur}')
    cv2.imshow(windowName, mask)


cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)


def main(args):
    global image
    # load an image

    image_path = args.image_path

    image = cv2.imdecode(np.fromfile(image_path, np.uint8), cv2.IMREAD_UNCHANGED)
    if args.rgb_mask:
        cv2.createTrackbar(trackbarValue, windowName, scaleFactor, 255, scale_rgb)
        cv2.createTrackbar(blurValue, windowName, scale_blur, 100, scale_rgb)
    else:
        cv2.createTrackbar(trackbarValue, windowName, scaleFactor, 255, scale_hsv)
        cv2.createTrackbar(blurValue, windowName, scale_blur, 100, scale_hsv)


    # Create a window to display results

    # scale_hsv(2)

    while True:
        c = cv2.waitKey(20)
        if c == 27:
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Check threshold")
    parser.add_argument(
        "-i", "--image_path", dest="image_path",
        required=True,
        help="input path to a JPG file "
    )
    parser.add_argument(
        "-rgb", "--rgb_mask", default=False, action="store_true",
        help="RGB mask is choose"
    )
    args = parser.parse_args()
    main(args)
