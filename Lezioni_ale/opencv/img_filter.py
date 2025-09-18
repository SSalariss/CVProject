import numpy as np
import cv2

# Getting the image
img = cv2.imread("Esercitazioni\da_modificare\data\\tomb.jpg")

# Creating the kernel for the filter
kernel = np.array([
                    [0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]
])

filtered_img = cv2.filter2D(img, -1, kernel)
blured_img = cv2.blur(img, (21, 21))
median_img = cv2.medianBlur(img, 3)
gaussian_img = cv2.GaussianBlur(img, (9,9), 10)
unsharped_img = cv2.addWeighted(img, 1.5, gaussian_img, -0.5, 0)


cv2.imshow("Gaussian blur", gaussian_img)
cv2.imshow("Unsharped img", unsharped_img)
cv2.imshow("MedianBlur", median_img)
cv2.imshow("Img", img)
cv2.imshow("Filtered img", filtered_img)
cv2.imshow("Blured img", blured_img)
cv2.waitKey(0)
