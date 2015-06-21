#Import directory above tests
import sys
import os
import re
import importlib
sys.path.append('../')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import ward, dendrogram

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import nltk
import re
import mpld3
from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics.pairwise import cosine_similarity
import theano
import theanets
from sklearn.metrics import classification_report, confusion_matrix

import tasks
import utility
import pymongo
import code



def get_items(items):
	ids = []
	titles = []
	ds = []
	prices = []
	for i in range(0, 40):
		_id = items.find()[i]['item_id']
		center_html = items.find()[i]['html1']['CenterPanelInternal']
		center = tasks.parse_center(center_html)
		title = center['item_title'].lower()
		if center['price'] == None:
			continue
		_price = re.search('US \$(.*)', center['price'])
		if _price == None:
			continue
		price = float(_price.group(1).replace(',', ''))

		descr_html = items.find()[i]['html1']['vi-desc-maincntr']
		descr = tasks.parse_descr(descr_html)

		ids.append(_id)
		titles.append(title)
		ds.append(strip_tags(descr['specifics']).__str__().decode('utf-8'))
		prices.append(price)
	return titles, ds, prices


vectorizer = CountVectorizer(min_df=1)
X_train = vectorizer.fit_transform(t_titles)

tf_transformer = TfidfTransformer()
X_train_tf = tf_transformer.fit_transform(X_train)




def split_data(X, y, slices):
    '''
    Splits the data into training, validation and test sets.
    slices - relative sizes of each set (training, validation, test)
        test - provide None, since it is computed automatically
    '''
    datasets = {}
    starts = np.floor(np.cumsum(len(X) * np.hstack([0, slices[:-1]])))
    slices = {
        'training': slice(starts[0], starts[1]),
        'validation': slice(starts[1], starts[2]),
        'test': slice(starts[2], None)}
    data = X, y
    def slice_data(data, sl):
        return tuple(d[sl] for d in data)
    for label in slices:
        datasets[label] = slice_data(data, slices[label])
    return datasets




datasets = split_data(X, y, (0.6, 0.2, None))

exp = theanets.Experiment(
    theanets.Classifier,
    # (input dimension, hidden layer size, output dimension = number of classes)
    layers=(2, 2, 2),
    hidden_l1=0.1)


exp.train(
    datasets['training'],
    datasets['validation'],
    optimize='sgd',
    learning_rate=0.01,
    momentum=0.5)



X_test, y_test = datasets['test']
y_pred = exp.network.classify(X_test)

print('classification_report:\n', classification_report(y_test, y_pred))
print('confusion_matrix:\n', confusion_matrix(y_test, y_pred))
