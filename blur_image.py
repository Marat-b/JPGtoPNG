import cv2

image_path = 'Y:\\UTILZ\\MaskRCNN\\potato\\set4\\0_100.jpg'
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
blured = cv2.blur(img, (10, 10))
cv2.imshow('im', blured)
# cv2.imwrite('im.png', im)
if cv2.waitKey(50000) == 27:
    pass
