import code
import sys
import os
import re
import importlib
import pickle
sys.path.append('../')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import numpy as np
import matplotlib.pyplot as plt
import climate # some utilities for command line interfaces
import theanets
from sklearn.metrics import classification_report, confusion_matrix

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import nltk
import re
import mpld3
from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics.pairwise import cosine_similarity

import tasks
import utility
import pymongo

climate.enable_default_logging()
settings = importlib.import_module('MAC_SETTINGS')
category = '9355'
conn = utility.get_mongo_connection()
item_coll = utility.get_collection(category, 'items', conn)

def get_items(items):
	titles = []
	#ds = []
	solds = []
	#prices = []

	N_samples = 2000

	x = 0; z = 0; i = -1
	while x < N_samples or z < N_samples:
		i += 1

		center_html = items.find()[i]['html1']['CenterPanelInternal']
		center = tasks.parse_center(center_html)
		title = center['item_title']
		if center['bids'] == None:
			continue
		bids = int(center['bids'])
		sold = int(not bids == 0)

		print sold, x, z

		if sold == 1 and x < N_samples:
			titles.append(title)
			solds.append(sold)
			x += 1
		elif sold == 0 and z < N_samples:
			titles.append(title)
			solds.append(sold)
			z += 1
		else:
			continue

	return titles, solds


	#for i in range(0, 1000):
		#center_html = items.find()[i]['html1']['CenterPanelInternal']
		#center = tasks.parse_center(center_html)
		#title = center['item_title']
		#if center['bids'] == None:
		#	continue
		#bids = int(center['bids'])
		#sold = int(not bids == 0)

		#_price = re.search('US \$(.*)', center['price'])
		#if _price == None:
		#	continue
		#price = float(_price.group(1).replace(',', ''))

		#descr_html = items.find()[i]['html1']['vi-desc-maincntr']
		#descr = tasks.parse_descr(descr_html)

		#titles.append(title)
		#solds.append(sold)
		#ds.append(strip_tags(descr['specifics']).__str__().decode('utf-8'))
		#prices.append(price)
	#return titles, solds


def split_dataset(dataset):
	vecs = dataset[0]
	labels = dataset[1]

	training_set = [[], []]
	testing_set = [[], []]

	#Use ratio of 80 20 for training + testing sets
	m = len(vecs)
	j = int(m * 0.8)

	training_set[0] = vecs[0:j]
	training_set[1] = labels[0:j]

	testing_set[0] = vecs[j:m]
	testing_set[1] = labels[j:m]

	return training_set, testing_set


#X is the vector y is the label
#titles, solds = get_items(item_coll)

#label0 = [[], []]
#label1 = [[], []]
#for i in range(0, len(titles)):
#	if solds[i] == 0:
#		label0[0].append(titles[i]); label0[1].append(solds[i])
#	else:
#		label1[0].append(titles[i]); label1[1].append(solds[i])

#_titles = []; _solds = []
#for i in range(0, len(label0[0])):
#	_titles.append(label0[0][i]); _solds.append(label0[1][i])
#	_titles.append(label1[0][i]); _solds.append(label1[1][i])


#__titles = CountVectorizer(min_df=1).fit_transform(_titles)
#titles_tf = TfidfTransformer().fit_transform(__titles)

#titles_tf = titles_tf.todense().astype(np.float32)
#solds = np.array(_solds).astype(np.int32)

#dataset = (titles_tf, solds)
#f = open('./dataset.pickle', 'w')
#pickle.dump(dataset, f)
#f.close()


with open('./dataset.pickle', 'U') as f:
	dataset = pickle.load(f)

training_set, testing_set = split_dataset(dataset)

input_dimity = len(dataset[0][0].tolist()[0])

exp = theanets.Experiment(
    theanets.Classifier,
    layers=(input_dimity, 2, 2),
    hidden_l1=0.1)
exp.train(
    training_set,
    training_set,
    optimize='sgd',
    learning_rate=0.01,
    momentum=0.5,
    patience=40)



X_test, y_test = testing_set
y_pred = exp.network.classify(X_test)

print('classification_report:\n', classification_report(y_test, y_pred))
print('confusion_matrix:\n', confusion_matrix(y_test, y_pred))


code.interact(local=locals())


