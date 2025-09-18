# import the dataset
from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

import seaborn as sns
import matplotlib.pyplot as plt

# pick a subset of categories (for semplicities)
categories = ['talk.religion.misc', 'sci.space', 'comp.graphics']

# load the data
train = fetch_20newsgroups(subset='train', categories=categories)
test = fetch_20newsgroups(subset='test', categories=categories)

# create the model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# train the model
model.fit(train.data, train.target)
y_pred = model.predict(test.data)

# create the confusion matrix
mat = confusion_matrix(test.target, y_pred)

# plot the confusion matrix
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False, xticklabels=train.target_names, yticklabels=train.target_names)
plt.xlabel('True Labels')
plt.ylabel('Predicted Labels')
plt.show()