import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns



iris = sns.load_dataset('iris')

sns.pairplot(iris, hue='species')

#* Note:
# in the machile learning, the X stands for 
# all the features but without the label,
# otherwise y stands for the label 
# so we are separating the X for the y
# in this example.

#* Note:
# seaborn use pandas module

# delete the label column from the dataset
X_iris = iris.drop('species', axis=1)   #? axis=1 indica che 'species' è una colonna

# create the list containing the labels
y_iris = iris['species']

# split the dataset into trainint set and
# test set
Xtrain, Xtest, ytrain, ytest = train_test_split(X_iris, y_iris)
# we could use train_size variables [0, 1] to change the size of the train dataset


"""
Il modello GaussianNB è ottimo quando abbiamo una distribuzione lineare
"""
# instatiate the model
model = GaussianNB()

# train the model
model.fit(Xtrain, ytrain)

# do the prediction
y_pred = model.predict(Xtest)

# check how good is our model
accuracy = accuracy_score(ytest, y_pred)

"""
? Distribuzione dei valori lunghezza petali
plt.figure(figsize=(10, 6))
x_vals = np.linspace(0, 2.5, 100)

for i, class_name in enumerate(iris['species'].unique()):
    mu = model.theta_[i, 3]  # petal width è la 4a feature (indice 3)
    sigma = model.var_[i, 3]
    plt.plot(x_vals, 
             1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x_vals - mu)/sigma)**2),
             label=f'{class_name} (μ={mu:.2f}, σ={sigma:.2f})')

plt.xlabel('Petal Width (cm)')
plt.ylabel('Densità di probabilità')
plt.title('Distribuzioni stimate da GaussianNB')
plt.legend()
plt.show()

Tramite questo grafico possiamo vedere che le gaussiane sono bel distribuite,
non sovrapposte e discriminative (curve molto rapide), quindi il modello GaussianNB
si comporta molto bene.
"""


#* Regressione Lineare:
"""
? A cosa serve
La regressione lineare serve a:
    - Prevedere valori CONTINUI nel tempo (prezzo di una casa in base ai m^2)
    - Capire la relazione tra la variabile x e la variabile y
    - Trovare la miglior retta che approssima i dati

? Come funziona
La regressione lineare cerca di trovare una retta y = mx + b dove:
    - y è il valore da prevedere (es. prezzo di una casa)
    - x è il la variabile in input (es. metri quadri)
    - m è il coefficente angolare (quanto cambia y al cambiare di x)
    - b è l'intercetta, cioè il valore di y quando x = 0
Usando il metodo dei MINIMI QUADRATI, possiamo minimizzare l'errore tra i punti reali
e quelli previsti dal modello:
          n
Errore = SUM  (y_vero - y_prev)^2
          i=1
Tramite questa formula possiamo trovare una retta che si avvicina il più possibile ai punti reali.

? Quando usarlo
In conclusione possiamo dire che questo modello è efficace quando dobbiamo trattare problemi
semi-lineari o del tutto lineari:
    - Economia: Prevedere il prezzo di una casa (y) in base ai metri quadrati (x)
    - Medicina: Stimare l'aspettativa di vita (y) in base al numero di sigarette fumate al giorno (x).
    - Marketing: Prevedere le vendite (y) in base al budget speso in pubblicità (x).

? Problemi complessi
Per problemi più complessi che non possono adattarsi ad una semplice retta (funzioni periodice come sin) ci sono
modelli più complicati che prevedono polinomi invece che rette
"""
# creating the random generator between 0 and 1 with seed 42
rng = np.random.RandomState(42)


"""
? Cosa stiamo facendo
Stiamo creando 50 punti:
    - x: valore tra 0 e 1 moltiplicato per 10 [0, 10]
    - y: descrive la retta 2x - 1 (mx + b) ma aggiunge del "suono" per
        simulare la realtà
Avremo quindi dei punti che si simulano l'andamento di una retta 2x - 1 ma,
un po' come la realtà, avremo valori leggermente sfasati grazie al suono ( +rng.rand(50) )

? Risultato
Come risultato avremo che il modello avrà calcolato una retta con:
    m circa 2
    b circa -1
"""
# create fake data
x = 10 * rng.rand(50)
y = 2 * x-1 + rng.rand(50)

"""
? fit_intercept
Con fit_intercept diciamo che il modello deve trovare il valore
di b, se fosse falso allora il modello cerca soltano m creando una retta
con y = 0 se x = 0
Ad esempio una casa con 0 metri quadri non varrà mai 0 euro.
"""
# model instance
model = LinearRegression(fit_intercept=True)

"""
? np.newaxis
Dato che x è un array 1D, possiamo trasformarlo in una matrice
tramite np.newaxis, quindi x passerà da una forma (15,) a (15, 1)
Ad esempio:
[1, 2, 3] 
-->
[[1], 
 [2],
 [3]]
"""
# create the data matrix
X = x[:, np.newaxis]

# model training    
model.fit(X, y)

"""
Abbiamo quindi addestrato il modello con una x [0, 10], andiamo quindi
a creare 50 punti (valore di default di linspace) tra [-1, 11] andando quindi
fuori dai valori precedenti della x.
Facendo ciò abbiamo un dataset diverso da quello con cui è stato allenato il modello
rendendo il test più 'vero'

? np.newaxis
Ricordiamo che predict e fit vogliono array X 2D e non array monodimensionali.
"""

"""
* Cross validation
Stiamo eseguendo una cross validation suddividendo il dataset
in due parti, ma se volessimo eseguire un cross validation suddividendo
il dataset in 10 parti? (Usato anche nei paper)
Esiste una funzione che ci permette di farlo!

? OLD
# creating test data
x_fit = np.linspace(-1, 11)
X_fit = x_fit[:, np.newaxis]

# predict labels for new data
y_pred = model.predict(X_fit)
"""

"""
? plt.scatter
Utilizza i valori veri di x ed y come assi.

? plt.plot
Utilizza i valori dentro X_fit e y_pred per creare la retta

? plt.show
Mostra il grafico
"""
# visually see the prediction
plt.scatter(x, y)
plt.plot(X_fit, y_pred)
plt.show()



