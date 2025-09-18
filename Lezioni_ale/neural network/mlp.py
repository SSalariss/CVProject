from sklearn.neural_network import MLPClassifier # Multi layer perceptron
from sklearn.datasets import fetch_openml, load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# MNIST dataset
# constains handrawn digits from 0-9
# each digit is a 28x28 image gray scale

# download the dataset
#X, y = fetch_openml('mnist_784', return_X_y=True)
X, y = load_digits(return_X_y=True)

# create train ad test dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)

# create the model
model = MLPClassifier(hidden_layer_sizes=(20, 1))

# train the model
model.fit(X_train, y_train)

# test the model
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(accuracy)