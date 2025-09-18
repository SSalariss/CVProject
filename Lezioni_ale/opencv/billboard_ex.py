from typing import Any

import numpy as np
import cv2
from cv2.typing import MatLike, NumPyArrayFloat32, NumPyArrayNumeric

"""
? Cosa fa questo programma di preciso?
Abbiamo due immagini:
    - base_img
    - img2
Lo scopo è:
    1. Selezionare 4 punti in 'base_img'
    2. Inserire img2 nei 4 punti selezionati

? Soluzione
* - - - LOADINGS - - - 
1. Carico le due immagini 'base_img' e 'img2'

2. Ottengo una copia di 'base_img' con nome 'base_img_cpy' dato che NON voglio
    che i cerchi vengano scritti nella vera immagine

    
* - - - VARIABLES - - -
3. Ottengo altezza e larghezza di 'base_img'

4. Ottengo altezza e larghezza di 'img2'


* - - - POINTS - - - 
5. Creo i source point, come abbiamo detto vogliamo che TUTTA l'immagine 'img2' vada dentro
    i 4 punti di 'base_img' quindi i 4 punti saranno:
    [0     ,       0]    - - - - - - - - - - - - -  [    0   ,      'base_width']

            |                                                 |
            |                                                 |
            |                                                 |
            |                                                 |

    ['base_height, 0]    - - - - - - - - - - - - -  ['base_height', 'base_width']

6. Creo e converto in float32 i destination points che verranno selezionati dall'utente
    tramite l'evento "LBUTTONDOWN' che, una volta verificatosi, chiama
    la funzione 'onClick' grazie al fallback di 'base_img'.setMouseFallback

    
*- - - TRASFORMAZIONE 'img2' - - -
7. Calcolo la matrice H per l'homography, essa calcola la matrice H da applicare
    affinchè i punti 'source_points' diventino 'dst_points'

8. Creo un immagine 'warp' dove utilizzo la matrice H precedentemente calcolata
    per trasformare l'immagine affinchè entri nei punti selezionati dall'utente (dst_points)


* - - - MASCHERE - - -
9. Creo una maschera grante quanto 'base_img' completamente BINCA

10. Creo un poligono NERO in 'mask' con punti [dst_points]

11. Creo 'masked_billboard' che è un AND di bit tra 'mask' e 'base_img' ma cosa comporta?
    Ricordiamoci che 'mask' è BIANCA tranne nei punti [dst_points] -->
    ciò comporta che tutta 'base_img' sarà uguale [BIANCO] AND [Colore] = [Colore]
    TRANNE nei punti NERI [NERO] AND [Colore] = [NERO].
    Avremo quindi 'base_img' che ha un poligono nero nei [dst_points]

    
* - - - FINAL - - -
12. Infine creo 'final_img' che non è altro un OR bit a bit tra 'masked_billboard' e
    'warp', tutta l'immagine sarà uguale TRANNE nel poligono nero dove
    [Colore_warp] OR [NERO_masked_billboard] = [Colore_warp]
    Quindi tutta l'immagine sarà uguale tranne nel poligono nero che si convertirà
    nella nostra immagine 'warp' che non è altro 'img2' trasfigurata con la matrice H
"""

# La funzione gestisce l'evento LBUTTONDOWN che si
# presenza nella 'base_img' creando dei cerchi
# nella posizione del mouse
def onClick(event: int, pos_x: int, pos_y: int, flags: int , param: Any | None) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(dst_points) < 4:
            dst_points.append([pos_x, pos_y])
            cv2.circle(base_img_cpy, (pos_x, pos_y), 50, (0, 0, 255), -1)
            cv2.imshow("base img cpy", base_img_cpy)


# env
debug = True


# load the two images
base_img: MatLike = cv2.imread("Esercitazioni\opencv_lessons\data\\billboard.jpg")
img2: MatLike = cv2.imread("Esercitazioni\opencv_lessons\data\ezio.jpg")

# Copying the base image (i don't want modify the original image)
base_img_cpy: MatLike = base_img.copy()


# Getting base img sizes (width and height)
base_h,  base_w = base_img_cpy.shape[:2]
img2_h, img2_w = img2.shape[:2]

# Creating source and destination points
# src_points: the whole img2
# dst_points: selected by user 
src_points: NumPyArrayFloat32 = np.array([[0, 0], [0, img2_h], [img2_w, img2_h], [img2_w, 0]], dtype=np.float32)
dst_points: NumPyArrayNumeric = []

# Resized the images
cv2.namedWindow("base img cpy", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("img2", cv2.WINDOW_KEEPRATIO)

# Settings the mouse fallback on the base image (cpy)
cv2.setMouseCallback("base img cpy", onClick)

# Showing images
cv2.imshow("base img cpy", base_img_cpy)
cv2.imshow("img2", img2)
cv2.waitKey(0)



#* Computing the homography matrix
# Converting the destination points in float32
dst_points_float: NumPyArrayFloat32 = np.array(dst_points, dtype=np.float32)

# Getting the (H)omography matrix from src_points into destination points
# H: matrix to apply at src_points to getting dst_points_float
H: MatLike = cv2.getPerspectiveTransform(src_points, dst_points_float)

# Applying the (H)omography matrix
# so we are trasforming 'img2' from src_points --> dst_points_float
warped: MatLike = cv2.warpPerspective(img2, H, (base_w, base_h))

#* MASK
# Create a mask with shape as base img shape filled with WHITE color
mask: NumPyArrayNumeric = np.full(base_img.shape, fill_value=(255, 255, 255), dtype=np.uint8)

# Create a polygon with destination points as points and WHITE color
cv2.fillConvexPoly(mask, np.int32(dst_points), (0, 0, 0))
if debug:
    cv2.namedWindow("mask", cv2.WINDOW_KEEPRATIO)
    cv2.imshow("mask", mask)
    cv2.waitKey(0)

 
# Now mask have all WHITE pixels except a polygon with
# all BLACK pixels, so what does this mean?
# with an bitwise_and with 'mask' and 'base_img'
# we can save all the 'base_img' EXCEPT from the black
# polygon that remain black.
# Remember that:
# [WHITE] AND [Color] = [Color]
# [BLACK] AND [Color] = [BLACK]
# So we can create a 'masked_billboard' that rappresente this.
masked_billboard: MatLike = cv2.bitwise_and(base_img, mask)
if debug:
    cv2.namedWindow("masked_billboard", cv2.WINDOW_KEEPRATIO)
    cv2.imshow("masked_billboard", masked_billboard)
    cv2.waitKey(0)

# Final step is to bitwise_or 'masked_billboard' --> 'base_img' with black polygon
# and 'warped' --> 'img2' shaped like the black polython in 'masked_billboard'
# so all the img remains the same EXCEPT the black polygon that will have
# the same colors as 'warped' image.
# Remember that:
# [BLACK] OR [Color] = [Color]
# 'warped' is all BLACK except the polygon that contains all 'img2'
final_img: MatLike = cv2.bitwise_or(masked_billboard, warped)
cv2.namedWindow("final_img", cv2.WINDOW_KEEPRATIO)
cv2.imshow("final_img", final_img)
cv2.waitKey(0)
