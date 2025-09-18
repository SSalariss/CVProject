import cv2
import numpy as np

want_harris = False
want_sift = True

# loading image
img = cv2.imread("Esercitazioni\opencv_lessons\data\lena.png")

# downscaled image to demostrate that
# Harris IS NOT scale invariant
resized = cv2.resize(img, None, fx=0.5, fy=0.5)

# we don't need colors for image extractor
gray_img = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

if want_harris:

    # extract corners from images with Harris algorithm
    # dst è una matrice contenente dei valori (sia pos che neg)
    # che indicato il grado di "angolosità" R dove
    # R molto grande  --> angolo
    # R vicino a 0    --> zona piatta
    # R negativo      --> bordo
    dst = cv2.cornerHarris(gray_img, 2, 23, 0.04)

    # thresholding the corners for getting better ones
    resized[dst > 0.01 * dst.max()] = [0, 255, 0]

    result = resized


if want_sift:
    
    # Compute the Scale Invariant Feature Transform (SIFT)
    sift = cv2.SIFT.create()
    keypoints, descriptors = sift.detectAndCompute(img, None)

    orb = cv2.ORB.create()
    keypoints, descriptors = orb.detectAndCompute(img, None)

    akaze = cv2.AKAZE.create()
    keypoints, descriptors = akaze.detectAndCompute(img, None)

    # draw the keypoints
    cv2.drawKeypoints(img, keypoints, img, (255, 0, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


cv2.namedWindow("result", cv2.WINDOW_KEEPRATIO)
cv2.imshow("result", img)
cv2.waitKey(0)