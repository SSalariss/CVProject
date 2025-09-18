import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


# create the data
x = np.array([1,2,3,4,5])
y = np.array([4, 2, 1, 3, 7])

# enhance features
poly = PolynomialFeatures(degree=3)

X = x[:, np.newaxis]
X2 = poly.fit_transform(X, y)

print(X2)

model = LinearRegression().fit(X2, y)
y_pred = model.predict(X2)

plt.scatter(x, y)
plt.plot(x, y_pred)
plt.show()