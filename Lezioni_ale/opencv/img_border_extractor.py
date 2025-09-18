import cv2
import numpy as np

img = cv2.imread("Esercitazioni\da_modificare\data\salt_pepper.png", 0)

cv2.imshow("Before", img)

"""
? Using Sobel
# Compute the derivative
der_x = cv2.Sobel(img, -1, 1, 0)
der_y = cv2.Sobel(img, -1, 0, 1)

# Derivative absolute values (pixels can't have negative colors)
abs_x = cv2.convertScaleAbs(der_x)
abs_y = cv2.convertScaleAbs(der_y)

# Adding the derivative on the x and y axies
der_total = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
"""
# Here we can calculate the seconda grade derivative in both axies
# ksize = kernel size
# more size --> more details but not consistent with sound
# less size --> general form but more consistent
der_tot = cv2.Laplacian(img, -1, ksize=1)

# Convert in absolute values (pixels cannot have negative values)
abs_der = cv2.convertScaleAbs(der_tot)

cv2.imshow("After", abs_der)
cv2.waitKey(0)
