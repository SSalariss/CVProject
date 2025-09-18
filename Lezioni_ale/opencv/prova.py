import numpy as np
import cv2

"""
x = np.array([[250]], dtype=np.uint8)
y = np.array([[50]], dtype=np.uint8)

print("OpenCV add:", cv2.add(x, y)) # saturazione a 255
print("NumPy add:", x + y)          # overflow modulo 256
"""

img = cv2.imread("Esercitazioni\da_modificare\data\\tomb.jpg")
img2 = np.zeros(img.shape, dtype=np.uint8)
masked = cv2.circle(img2, (200, 200), 300, (255, 255, 255), -1)


land_img = cv2.bitwise_and(img, masked)
lor_img = cv2.bitwise_or(img, masked)
lxor_img = cv2.bitwise_xor(img, masked)
lnot_img = cv2.bitwise_not(img, masked)

cv2.imshow("land", land_img)
cv2.imshow("lor", lor_img)
cv2.imshow("lxor", lxor_img)
cv2.imshow("lnot", lnot_img)
cv2.waitKey(0)
