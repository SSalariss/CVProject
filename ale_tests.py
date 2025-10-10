import cv2
import numpy as np

want_local_pixel_distribution = True
want_hsv = True


img_org = cv2.imread("Esercitazioni\opencv_lessons\data\giocatori.jpeg")


img = cv2.cvtColor(img_org, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img)
eq_v = cv2.equalizeHist(v)
equalized = cv2.merge([h, s, eq_v])


# Definisci il range del verde in HSV
lower_green = np.array([35, 50, 50])   # H, S, V min
upper_green = np.array([85, 255, 255]) # H, S, V max

# Crea la maschera
mask = cv2.inRange(equalized, lower_green, upper_green)

# Applica la maschera all'immagine originale
result = cv2.bitwise_and(equalized, equalized, mask=mask)

img_rgb = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

der_tot = cv2.Laplacian(img_rgb, -1, ksize=3)

# Convert in absolute values (pixels cannot have negative values)
abs_der = cv2.convertScaleAbs(der_tot)

# ===============================
# PARAMETRI MODIFICABILI
# ===============================
tolleranza = 200                # Valore di soglia per rilevare linee nette (0-255)
min_line_length = 200           # Lunghezza minima della linea
max_line_gap = 50              # Massimo gap tra segmenti di linea

# ===============================
# CARICAMENTO E PREPARAZIONE IMMAGINE
# ===============================
gray = cv2.cvtColor(abs_der, cv2.COLOR_BGR2GRAY)      # Convertiamo in scala di grigi
blur = cv2.GaussianBlur(gray, (5,5), 0)          # Applichiamo un leggero blur per ridurre rumore

# ===============================
# RILEVAMENTO BORDI
# ===============================
edges = cv2.Canny(blur, tolleranza, tolleranza * 2, L2gradient=True)  # Rilevamento bordi con soglia modificabile

# ===============================
# RILEVAMENTO LINEE CON Hough Transform
# ===============================
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=min_line_length, maxLineGap=max_line_gap)

# ===============================
# DISEGNO DELLE LINEE SULL'IMMAGINE
# ===============================
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img_org, (x1, y1), (x2, y2), (0, 0, 255), 2)

res = cv2.resize(img_org, (1200,600), interpolation=cv2.INTER_LINEAR)

# ===============================
# MOSTRA RISULTATI
# ===============================
cv2.imshow("Linee Rilevate", img_org)
#cv2.imshow("Bordi", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()





