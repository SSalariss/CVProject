import cv2
import numpy as np


# Loading the two images for building the panorama
right = cv2.imread("Esercitazioni\opencv_lessons\data\\right.png")
left = cv2.imread("Esercitazioni\opencv_lessons\data\left.png")


cv2.namedWindow("right", cv2.WINDOW_KEEPRATIO)
cv2.imshow("right", right)

cv2.namedWindow("left", cv2.WINDOW_KEEPRATIO)
cv2.imshow("left", left)

cv2.waitKey(0)

# create an instance of ORB (faster but less precised)
orb = cv2.ORB.create()

# compute the features in both the images
kpts_left, descr_left = orb.detectAndCompute(left, None)
kpts_right, descr_right = orb.detectAndCompute(right, None)


# we match the keypoints through knn algorithm (bruteforce matcher)
"""
? Ma cosa sono questi match?
* NOTA BENE: è importante allineare l'immagine 'destra' a quella di 'sinistra' e non il contrario
* affinchè poi possiamo incollare l'immagine 'sinistra' da (0,0) fino a left.shape.
* verrà in modo naturale l'immagine panorama dato che la parte di 'sinistra' farà overlap delle parti in comune
Un match non è altro che una SOMIGLIANZA tra le due descrizioni,
ad esempio supponiamo di avere in descr_right:
[..., 1, 1, 1, 0, 0, 1, 0, ...]
Abbiamo due miglior match in descr_left:
[..., 1, 1, 0, 0, 0, 0, 1, ...]     Con "distanza" = 2
[..., 1, 1, 1, 0, 0, 0, 0, ...]     Con "distanza" = 1
Con "distanza" intendiamo "quanti bit sono diversi da descr_right?"

! PROBLEMA
Se abbiamo due match MOOLTO simili, in questo caso abbiamo che la loro differenza è
2 - 1 = 1, abbiamo che, in due punti diversi dell'immagine, abbiamo un match ma ciò è
molto ambiguo e quindi bisognerebbe scartare questi due match, ecco perchè si utilizza una certa
soglia MINIMA, ad esempio possiamo accettare un match m1 sse il prossimo match migliore dopo m1,
chiamato m2 ha una certa distanza minima, quindi se m1 = x e m2 = y allora prendiamo m1 sse
distanza(m1) - distanza(m2) è maggiore di un certo numero, ad esempio 40.
Ciò rende più consistente il match scartando i "finti positivi"
Questo appena spiegato è proprio ciò che fa 'knnMatch' che estrae i k(=2 in questo caso) match
migliori.

? Cos'è BFMatcher e perchè si utilizza cv2.NORM_HAMMING?
BFMatch sta per Brute-Force Matching ed è un algoritmo di matching,
che confronta TUTTI i descrittore di un immagine con TUTTI i descrittori
dell'altra immagine per trovare le corrispondenze migliori.

? NORM_HAMMING
Qui stiamo dicendo che:
    - Stiamo utilizzando descrittori binari (come ORB, BRIEF, BRISK...)
    - La distanza usata per il confronto è la DISTANZA DI HAMMING

? Distanza di NORM_HAMMING
Conta semplicemente quanti bit differiscono tra due descrittori, perfetta
per descrittori binari.

? E se non voglio usare BFMatcher?
Esistono altri algoritmi come FLANN molto più rapidi con dataset grandi
(BFMatcher ha O(n^2) mentre FLANN utilizza strutture dati molto più veloci come KD-Trees)

? knnMatch?
Semplicemente ordina in modo crescente tutte le distanze dei descrittori e 
prende i k più migliori per poter eseguire il ratio test.
Esiste anche la funzione match che estrae direttamente la migliore ma così non possiamo
effettuare test come il 'ratio test'


? Dubbio frequente
Ma quanti match ho? se ho k=2 ho solo due match? NO
Chiarezza su 'kpts, descr':
sono due LISTE dove ogni keypoint in ktps ha associato un
descrittore in descr, quindi ktps[0] --> descr[0].
Cosa fa knnMatch con k = 2? Associa ad ogni
descr[0] di un immagine, ad esempio, 'left'
i DUE MIGLIORI descrittore che però appartengono all'immagine 'right'.
Quindi avremo che descr_left[0] avrà [descr_right1, descr_right2] cioè
i due migliori trovati nell'immagine 'right' per il descrittore 'left'.

"""
matcher = cv2.BFMatcher.create(cv2.NORM_HAMMING)
matches = matcher.knnMatch(descr_right, descr_left, 2)

# ratio test: the probability that a match
# is correct is determined by the computing
# the ratio of the distance from the closest
# neightborhood with the distance of the second
# closest neighborhood.
good_matches = []

"""
Ricordiamo che in matches abbiamo delle distanza ordinate
in modo crescente, ciò significa che m sarà sempre minore o uguale ad n
ma a noi interessa che M sia minore uguale ALMENO di un tot rispetto a n,
ad esempio vogliamo che M sia minore del 3% di N, quindi che
m < 0.03 * N
m = 0, n = 10
0 < 0.03 * 10 ==> 0 < 0.3
In generale 0.03 è moltro STRETTO come valore, praticamente accettiamo
solo match PERFETTI (quindi che sono moolto vicini allo 0 o proprio 0).
Tali match vengono inseriti nella lista dei "good_matches"
"""
for m, n in matches:  
    if m.distance < 0.05 * n.distance:
        good_matches.append(m)


"""
Qui dobbiamo tener conto degli attributi di m,
m.queryIdx: keypoint di m associato all'immagine 'query', cioè la 'prima'
m.trainIdx: keypoint di m associato all'immagine 'train', cioè la 'seconda'.
In pratica stiamo considerando sempre gli m matches migliori e da questi m
estraiamo i punti (x, y) della prima immagine e i punti (x, y) della seconda immagine.
è come se stessimo dicendo "guarda che left(x, y) e right(x', y') sono praticamente uguali!
kpts_left[m.queryIdx] dato che kpts_left è una lista, m.queryIdx ritorna l'id associato ad m, mentre
kpts_left[m.queryIdx].pt estrae i valori (x, y) associati a quel keypoint
"""
# check if we have at least 4 points for computing
# the homography
if len(good_matches) >= 4:
    
    # convert the keypoints to float32
    src_points = np.float32([kpts_right[m.queryIdx].pt for m in good_matches])
    dst_points = np.float32([kpts_left[m.trainIdx].pt for m in good_matches])

    """
    Qui abbiamo una cosa un po' ambigua, il test RANSAC, questo test
    rimuove anch'esso i punti ambigui, ma cosa fà di diverso?
    Ratio test: rimuove i punti ambigui 'localmente', un esempio potrebbe essere
    che il ratio test confronta le facce degli studenti e tiene solo quelle molto simili
    RANSAC: verifica che la loro POSIZIONE RELATIVA sia consistente, ad esempio il fratello A
    è sempre a destra del fratello B ANCHE DOPO la trasformazione geometrica. Tiene quindi conto
    della consistenza GEOMETRICA.

    5.0 non è altro che una soglia di errore per classificare un pixel valido.
    """
    M, mask = cv2.findHomography(src_points, dst_points)

    # Apply the M matrix in the 'right' image and resize the image with
    # column = right.column + left.column
    # rows = left.rows
    result = cv2.warpPerspective(right, M, (right.shape[1]+left.shape[1], right.shape[0]))
    result[0:left.shape[0], 0:left.shape[1]] = left.copy()

    

    cv2.namedWindow("result", cv2.WINDOW_KEEPRATIO)
    cv2.imshow("result", result)
    cv2.waitKey(0)
