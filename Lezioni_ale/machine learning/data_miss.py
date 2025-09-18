from sklearn.impute import SimpleImputer

from numpy import nan
import numpy as np

X = np.array([
    [nan, 0, 3],
    [3, 5, 2],
    [7, 9, nan]
    ])

y = np.array(
    [14, 16, 8]
)

imputer = SimpleImputer(strategy='mean')
X2 = imputer.fit_transform(X)

print(X2)

