import numpy as np
import time 

"""
! How to inizialize an np arrays
? Random arrays inizializers
x = np.array([0, 1, 2, 3], dtype=np.float32)
x2 = np.array([range(i, i+3) for i in [2, 4, 6]])

? Inizializzare array con 7 elementi, valore standard = 0 e tutti float32
x = np.zeros(7, dtype=np.float32)

? Oppure standard = 1
np.ones(7, dtype=np.int32)

? Oppure inizializzare una matrice 3 righe x 2 colonne con 1 di tipo int32
np.ones( (3, 2), dtype=np.int32)

? Inizializzo una matrice 3x2 con il valore 25 tramite la funzione fill
np.full( (3, 2), 25)

? Suddividiamo i numetri da 0 e 1 in 5 intervalli -> [0, 0.25, 0.5, 0.75, 1]
np.linspace(0, 1, 5)

? Inizializza una matrice 2x2 con numeri causali 
? stessa cosa utilizzando random.normal utilizzando la
? distribuzione normale.
? Se ci interessano valori randomici INTERI allora 
? possiamo utilizzare random.randint
np.random.random((2, 2))

? Crea una matrice quadrata con 1 nella diagonale principale.
? In questo caso crea una matrice 3x3:
? 1 0 0
? 0 1 0
? 0 0 1
np.eye(3)

? np.empy non crea un array VUOTO, ma bensì un array inizializzato
? in un'area di memoria non usata ma che potrebbe contenere valori.
? è un modo rapido per creare un array
np.empy(3)

? Utilizziamo il seed per debugging
np.random.seed(0)

? Con array creati tramite numpy possiamo accedere
? agli item tramite questa sintassi
array[1][0] -> array[1, 0]
array[:2][:3] -> array[:2, :3]



? Possiamo riconfigurare una nuova forma per l'array
? passando da una forma monodimensionale:
? [1, 2, 3, 4, 5, 6, 7, 8, 9]
? in una matrice 3x3
? [[1, 2, 3],
?  [4, 5, 6],
?  [7, 8, 9]]
x = np.arange(1, 10)
two_dim = x.reshape( (3, 3) )

? Voglio 2 row e non mi interessa quante
? colonne ci saranno, se non sarà possibile ottenere
? una matrice 2x? con tot valori darà ValueError.
two_dim = x.reshape( (2, -1) )
"""


"""
# 23.01 seconds to run with size = 10.000.000
def reciprocal(values):
    output = np.empty(len(values))
    for i in range(len(values)):
        output[i] = 1.0 / values[i]

values = np.random.randint(1, 10, size=10_000_000)

start = time.time()
#reciprocal(values)     # 23.01 seconds with standard loops
result = 1.0 / values   # Equivalent but in numpy 0.04 seconds DAFUQ
print(time.time() - start)
"""



