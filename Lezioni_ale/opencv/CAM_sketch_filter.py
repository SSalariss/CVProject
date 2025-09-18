import numpy as np
import cv2

# load the image to cartoonize
# img = cv2.imread("Esercitazioni\opencv_lessons\data\ezio.jpg")

# i want to use videocamera
cap = cv2.VideoCapture(0)

while True:

    # read current frame
    img = cap.read()[1] #? why 1? couse the first value is a bool that is True if is able to read

    # convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply median blur to remove noise
    img_gray = cv2.medianBlur(img_gray, 5)

    # extract the edges with Sobel or Laplacian
    edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=5) # ? 8U means 8bit unsigned

    # thresholding the eges
    # ? what thresholding means?
    # thresholding is the simplest method to segment an gray scale image
    # into a binary image, if the pixel [x, y] is less that T called threshold
    # than is black, otherwise is white
    # in this case everything above 70 is setted to 255
    _, threshold = cv2.threshold(edges, 70, 255, cv2.THRESH_BINARY_INV) #? THRESH_BINARY_INV invert the colors

    # get the colors with the bilateral filter
    color_img = cv2.bilateralFilter(img, 10, 250, 255)

    # merge color and edges
    skt = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
    sketch_img = cv2.bitwise_and(color_img, skt) #? why and? couse and will remain black pixels black

    # creating the window
    cv2.namedWindow("final img", cv2.WINDOW_KEEPRATIO)
    cv2.imshow("final img", sketch_img)
    key = cv2.waitKey(50) 

    # if we press q we will stop the cycle
    if key == ord('q'):
        break