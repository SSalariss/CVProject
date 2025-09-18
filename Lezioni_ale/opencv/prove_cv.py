import cv2
import numpy as np

# Posso aprire immagini 'png' e scrivere in 'jpg'
# openCV si occupa della conversione
# ! Il formato non è rgb ma bgr
# (b, g, r) = img[0,0]

"""
! Vari test con le immagini
canvas = np.zeros((500, 500, 3), dtype='uint8')

green = (0, 255, 0)
cv2.line(canvas, (0,0), (255,255), green, 4)

red = (0, 0, 255)
cv2.rectangle(canvas, (50, 50), (200, 200), red, -1)
#print(f'blue: {b}, green: {g}, red: {r}')

centerx, centery = canvas.shape[1]//2, canvas.shape[0]//2

cv2.circle(canvas, (centerx, centery), 30, (255,255, 255), -1)
cv2.circle(canvas, (centerx, centery), 30, (255, 0, 0), 2)

centerx, centery = img.shape[0]//2, img.shape[1]//2

print(f"pixels values of each channels are: {b[centerx, centery]} {g[centerx, centery]} {r[centerx, centery]}")

(b, g, r) = cv2.split(img)

img1 = cv2.merge( (g, r, b) )
img2 = cv2.merge( (r, g, b) )
img3 = cv2.merge( (b, g, r) )

cv2.imshow("OpenCV image", img1)
cv2.imshow("OpenCV image2", img2)
cv2.imshow("OpenCV image3", img3)
"""
"""

height, width = img.shape[:2]

print(img[0])

point1 = np.float32([[135, 45], [200, 80], [155, 200]])
point2 = np.float32([[200, 70], [250, 100], [175, 210]])
 
M = cv2.getAffineTransform(point1, point2)

print(M)
"""
"""
dst_img = cv2.warpAffine(img, M, (1000, 1000))

cv2.imshow("Image", dst_img)
cv2.waitKey(0)

# Carica un'immagine (puoi sostituire 'your_image.jpg' con il tuo file)
img = cv2.imread('Esercitazioni\da_modificare\data\ezio.jpg')
rows, cols = img.shape[:2]

# 3 punti sull'immagine originale
src_points = np.float32([[50, 50], [200, 50], [50, 200]])

# 3 punti sull'immagine trasformata (proviamo a ruotare + traslare)
dst_points = np.float32([[70, 70], [220, 80], [70, 230]])

# Calcola la trasformazione affine
M = cv2.getAffineTransform(src_points, dst_points)

# Applica la trasformazione
transformed = cv2.warpAffine(img, M, (cols*2, rows*2))

# Visualizza il risultato
cv2.imshow("Originale", img)
cv2.imshow("Trasformata (Affine)", transformed)
"""

"""
img = cv2.imread('Esercitazioni\da_modificare\data\gerry.png')

# Creatin starting point set
src_point = np.array([
                        [28, 227],  # Top left
                        [131, 987], # Bottom left
                        [730, 860], # Bottom right
                        [572, 149]  # Top right
], dtype=np.float32)    # If the type is integer won't work


# Destination point
dst_point = np.array([
                        [0, 0],
                        [0, 800],
                        [600, 800],
                        [600, 0]
], dtype=np.float32)

# Compute the homography matrix
H = cv2.getPerspectiveTransform(src_point, dst_point)

# apply H to original matrix
out_img = cv2.warpPerspective(img, H, (600, 800))

# Create windows and show the images
cv2.namedWindow("Img", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Output", cv2.WINDOW_KEEPRATIO)

cv2.imshow("Img", img)
cv2.imshow("Output", out_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
"""
