#Import directory above tests
import sys
import importlib
sys.path.append('../')

import tasks
import utility
import pymongo
import code

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


settings = importlib.import_module('MAC_SETTINGS')
category = '9355'
conn = utility.get_mongo_connection()
items = utility.get_collection(category, 'items', conn)

def get_cond_indices(conditions):
	possible_cs = {}
	for cond in conditions:
		if not cond in possible_cs.keys():
			possible_cs[cond] = len(possible_cs)
	return possible_cs

def get_cond_indice(condition, indices):
	indices[condition]


#Data preprocessing and feature extraction
conditions = []
for i in range(0, 100):
	center_html = items.find()[i]['html1']['CenterPanelInternal']
	center = tasks.parse_center(center_html)

	conditions.append(center['condition'])
c_indices = get_cond_indices(conditions)



features_list = []
targets = []

#Create feature table
for i in range(0, 100):
	center_html = items.find()[i]['html1']['CenterPanelInternal']
	center = tasks.parse_center(center_html)

	try:
		s_rating = int(center['seller_rating'])
	except Exception as e:
		continue

	condition = c_indices[center['condition']]
	n_images = len(center['images'])
	#features = [s_rating, condition, n_images]
	features = [n_images]

	sold = None
	if int(center['bids']) > 0:
		sold = 1
	elif int(center['bids']) <= 0:
		sold = 0
	target = sold
	features_list.append(features); targets.append(target)

print features_list

clf = MultinomialNB()
clf.fit(features_list, targets)

code.interact(local=locals())
