import cv2

file_src = r'Y:\UTILZ\MaskRCNN\potato\set4\input\backgrounds\photo_2022-03-14_13-53-49.jpg'
# file_dst = r'Y:\UTILZ\MaskRCNN\potato\set4\input\backgrounds\background_1.jpg'
file_src = r'Y:\UTILZ\MaskRCNN\potato\set2\0_100.jpg'

image = cv2.imread(file_src, cv2.IMREAD_UNCHANGED)
new_image = cv2.resize(image, (600, 600))
# cv2.imwrite(file_dst, new_image)
cv2.imshow('new', new_image)
cv2.waitKey()
