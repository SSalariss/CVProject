import numpy as np
import cv2


# Callback function
def onClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(src_points) < 4:
            src_points.append([x, y])
            cv2.circle(img_copy, (x, y), 10, (0, 0, 255), 1)
            cv2.imshow("Img", img_copy)




# Getting the image
img = cv2.imread("Esercitazioni\da_modificare\data\gerry.png")

# Creating the copy for the circles
img_copy = img.copy()

# Standard python list for coordinates
src_points = []

# Destination points
dst_points = np.array([
                        [0, 0],
                        [0, 800],
                        [600, 800],
                        [600, 0]
], dtype=np.float32)

# Img copy for choosing the 4 angles
cv2.namedWindow("Img", cv2.WINDOW_FREERATIO)

# Settings the mouse event fallback
cv2.setMouseCallback("Img", onClick)

# Showing the image copy
cv2.imshow("Img", img_copy)

# Wait 'enter' for the nexts computations
cv2.waitKey(0)

# Converting the src_points into numpy array float32
src_points_float = np.array(src_points, dtype=np.float32)

# Getting the homography
H = cv2.getPerspectiveTransform(src_points_float, dst_points)

# Creating the new output image
out_img = cv2.warpPerspective(img, H, (600, 800))

# Showing the output image
cv2.namedWindow("Out", cv2.WINDOW_FREERATIO)
cv2.imshow("Out", out_img)
cv2.waitKey(0)
