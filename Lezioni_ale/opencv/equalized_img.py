import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("Esercitazioni\opencv_lessons\data\\right.png")

want_bgr_image = False
want_gray_image = False
want_hsv = False
want_histo = False
want_local_pixel_distribution = True
want_test = False
"""
? Ma come funziona l'equalizzatore?
Supponiamo di avere la seguente immagine:
[50, 60, 60]
[70, 80, 80]
[90, 100, 100]
Tramite equalizzatore "stiriamo" i valori della matrice a tutti quelli
possibili, in questo caso [0, 255]. Il valore più basso, nel nostro esempio il 50,
assumerà il valore di (circa)0 mentre il valore più alto, nel nostro caso 100, assumerà il valore
di 255.
In realtà questo viene deciso da una formula che sfrutta il CDF (funzione di distribuzione cumulativa)
che esegue il seguente calcolo:
Valore      Frequenza       Probabilità             
50              1               1/9 = 0.111
60              2               3/9 = 0.333
70              1               4/9 = 0.444
80              2               6/9 = 0.666
90              1               7/9 = 0.777
100             2               9/9 = 1.000
Dove probabilità è la probabilità di trovare un'altro valore MINORE o UGUALE a quello corrente.
il nuovo valore è stabilito dalla seguente formula:
new_val = round(CDF[i] * (L - 1))
dove L è il numero di valori possibili, in questo caso 256, rendendo la formula:
new_val = round(CDF[i] * 255).
Quindi, ad esempio, il valore 50 diventerà:
50 = (0.111 * 255) = 28
mentre
100 = (1 * 255) = 255
"""
if want_test:
    img = np.array([
        [50, 60, 60],
        [70, 80, 80],
        [90, 100, 100]
    ], dtype=np.uint8)

    equalized = cv2.equalizeHist(img)


#* gray image case
if want_gray_image:
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    equalized = cv2.equalizeHist(img)

    equalized = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

#* bgr image case
if want_bgr_image:
    eq_channel = []
    channels = cv2.split(img)

    for ch in channels:
        eq_channel.append(cv2.equalizeHist(ch))

    equalized = cv2.merge(eq_channel)

#* hsv image case
if want_hsv:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(img)

    eq_v = cv2.equalizeHist(v)

    equalized = cv2.merge([h, s, eq_v])

    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

    equalized = cv2.cvtColor(equalized, cv2.COLOR_HSV2BGR)

#* histogram case
if want_histo:
    color = ('b', 'g', 'r')
    color_range = [0, 255]
    diagram_range = [0, 255]
    bin = [256]     # se fosse 64 avremmo che ogni bin copre 256 / 64 = 4 valori di intensità
    for i, col in enumerate(color):
        pass
        #channel = img[:,:,i] only visual purpose
        #plt.hist(channel.ravel(), 256, [0, 255], color=col) only visual purpose
        hist = cv2.calcHist([equalized], [i], None, bin, color_range)
        plt.plot(hist, color=col)

    plt.xlim(diagram_range) # the range of possibles values
    plt.show()



"""
We suddivide the image in smaller region and
apply the equalization for each region, with that
we can have a better result in images where we can't
cosinder all pixels as the same.
Example in data/tsukuba.

? Cosa cambia dal normale equalizzatore?
Qui abbiamo due valori:
clipLimit: valore di controllo, se ad esempio avessimo
[63, 63, 63,
 63, 63, 63,
 63, 63, 60]
tramite equalizzatore il 63 diventerebbe 255 e
60 diventerebbe 28 ma con una differenza così bassa
abbiamo un contrasto MOLTO forte, il clipLimit limita proprio questo!
Il 63 non verrà conteggiato più 8 volte ma bensì clipLimit volte al massimo!
E il resto? Viene distribuito su TUTTI i bin rimanenti.
Quindi il 60 diventerà 57 e il 63 diventerà 170 creando contrasti più morbidi.
In pratica, prendendo l'esempio dell'equalizzatore, il clipLimit limita il valore di
frequenza andando così a modificare il suo futuro valore.
"""
if want_local_pixel_distribution:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # CLAHE means Constast Limited Adaptive Histogram Equalization
    # clipLimit: 
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
    equalized = clahe.apply(img)
    equalized = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

#* Printing normal img and the equalized one
cv2.namedWindow("normal", cv2.WINDOW_KEEPRATIO)
cv2.imshow("normal", img)

cv2.namedWindow("equalized", cv2.WINDOW_KEEPRATIO)
cv2.imshow("equalized", equalized)
cv2.waitKey(0)