import cv2
import numpy as np

# ===============================
# PARAMETRI MODIFICABILI
# ===============================
image_path = "Esercitazioni\opencv_lessons\data\giocatori.jpeg"    # Percorso dell'immagine
tolleranza = 50                 # Valore di soglia per rilevare linee nette (0-255)
min_line_length = 200           # Lunghezza minima della linea
max_line_gap = 20              # Massimo gap tra segmenti di linea

# ===============================
# CARICAMENTO E PREPARAZIONE IMMAGINE
# ===============================
img = cv2.imread(image_path)
if img is None:
    raise ValueError("Immagine non trovata, controlla il percorso.")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)      # Convertiamo in scala di grigi
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
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# ===============================
# MOSTRA RISULTATI
# ===============================
cv2.imshow("Linee Rilevate", img)
cv2.imshow("Bordi", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
