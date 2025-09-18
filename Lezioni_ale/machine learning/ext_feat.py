from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd


"""
* DictVectorizer
data = [
    {'price': 12345, 'room': 4, 'neighborhood': 'Viale Ippocrate'},
    {'price': 87654, 'room': 6, 'neighborhood': 'Casilina'},
    {'price': 44444, 'room': 4, 'neighborhood': 'Appia'}
]

vec = DictVectorizer(dtype=int)
vec.fit_transform(data)

print(vec.get_feature_names_out())


Come posso convertire le stringhe 'neighborhood' in valori?

# {'Viale Ippocrate': 1, 'Casilina': 2, 'Appia': 3} BAD

Questa idea è sbagliata in quanto i numeri potrebbero indurre
un idea di 'classifica' dove numeri più alti 'valgono' di più.
Inoltre potremmo ottenere che 'Appia' - 'Casilina' = 'Viale Ippocrate'
che è completamente sbagliato.

Un'idea sarebbe quella di fare un 'one-hot encoding' trasformando ogni stringa in una 'feature'
rappresentata da una matrice dove, per ogni chiave del dizionario passato, viene aggiunta una colonna.
La colonna vale 1 sse è la stringa interessata mentre altri valori numerici rimangono tale.

                'Viale Ippocrate'       'Casilina'      'Appia'
'Viale Ippocrate'      1                    0              0
'Casilina'             0                    1              0
'Appia'                0                    0              1

Problema:
La matrice è densa e cresce molto rapidamente al crescere degli elementi nel dizionario.
"""

"""
* CountVectorizer
Convertiamo ogni stringa in una lista di occorrenze.
Ad esempio 'data' verrà rappresentata come:

        evil    horizon     of      problem     queen
0        1         0        1          1          0
1        1         0        0          0          1
2        0         1        0          1          0

Andando così a ridurre drasticamente il costo di memoria.

Ma come otteniamo la frase originale? Serve riottenerla?
"""
data = [
    'Problem of evil',
    'Evil queen',
    'Horizon problem'
]

vec = CountVectorizer()
X = vec.fit_transform(data)

# convert the vectorized datas to a pandas dataframe
vis_data = pd.DataFrame(X.toarray(), columns=vec.get_feature_names_out())

# TF-IDF = term frequency - inverse document frequency
vec2 = TfidfVectorizer()
X2 = vec2.fit_transform(data)
vis_data = pd.DataFrame(X2.toarray(), columns=vec2.get_feature_names_out())


print(vis_data)

