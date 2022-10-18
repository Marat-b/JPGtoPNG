import cv2
import numpy as np

from utils.cv2_imshow import cv2_imshow

# image_path = r'Y:\UTILZ\MaskRCNN\potato\store\in\set26\DSC_0614.JPG'
# image_path = 'Y:\\UTILZ\\MaskRCNN\\potato\\store\\in\\yandex\\Картошка фото\\20220418_101211.jpg'.encode(
#     'cp1251').decode('utf-8')
image_path2 = r"F:\VMWARE\FOLDER\UTILZ\MaskRCNN\potato\dataset\raw\train\strong5\DSC_0002.png"
print(image_path2)

# image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
image = cv2.imdecode(np.fromfile(image_path2, np.uint8), cv2.IMREAD_UNCHANGED)

# image = cv2.resize(image, (600, 402))
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
image_resized = image.copy()
# image_resized = cv2.resize(image_hsv, (300, 201))
# image_resized = image_resized[:, :280]

b_channel, g_channel, r_channel = cv2.split(image)[:3]
h_channel, s_channel, v_channel = cv2.split(image_hsv)[:3]
# h_channel_blurred = cv2.GaussianBlur(h_channel, (19, 19), 13, 13)
h_channel_blurred = cv2.blur(h_channel, (35, 35))
# h_channel_blurred = cv2.GaussianBlur(h_channel, (35, 35), 19, 19)
kernel = np.ones((12, 12), 'uint8')
erode_mask = cv2.erode(h_channel_blurred, kernel, cv2.BORDER_REFLECT, iterations=8)
dilate_mask = cv2.dilate(erode_mask, kernel, cv2.BORDER_REFLECT, iterations=10)
mask = cv2.threshold(dilate_mask, 30, 255, cv2.THRESH_BINARY_INV)[1]

kernel = np.ones((14, 14), 'uint8')
mask_bright = cv2.threshold(h_channel_blurred, 60, 255, cv2.THRESH_BINARY)[1]
erode_mask = cv2.erode(mask_bright, kernel, cv2.BORDER_REFLECT, iterations=3)
dilate_mask_2 = cv2.dilate(erode_mask, kernel, cv2.BORDER_REFLECT, iterations=5)

mask_united = cv2.bitwise_or(mask, dilate_mask_2)

# kernel = np.ones((2, 2), 'uint8')
# erode_mask = cv2.erode(mask, kernel, cv2.BORDER_REFLECT, iterations=4)
#
# dilate_mask = cv2.dilate(erode_mask, kernel, cv2.BORDER_REFLECT, iterations=5)
image_rgba = cv2.merge((r_channel, g_channel, b_channel, mask_united))

cv2_imshow(image, 'image')
cv2_imshow(h_channel, 'h_channel')
cv2_imshow(h_channel_blurred, 'h_channel_blurred')
cv2_imshow(s_channel, 's_channel')
cv2_imshow(v_channel, 'v_channel')
cv2_imshow(b_channel, 'b_channel')
cv2_imshow(g_channel, 'g_channel')
cv2_imshow(r_channel, 'r_channel')
# cv2_imshow(dilate_mask_2, 'dilate_mask_2')
cv2_imshow(mask, 'mask')
cv2_imshow(mask_bright, 'mask_bright')
cv2_imshow(mask_united, 'mask_united')
# cv2_imshow(erode_mask)
cv2_imshow(dilate_mask, 'dilate_mask')
cv2_imshow(image_rgba, 'image_rgba')
