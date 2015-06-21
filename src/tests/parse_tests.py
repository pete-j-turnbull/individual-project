#Import directory above tests
import sys
import importlib
sys.path.append('../')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

import tasks
import utility
import pymongo
import code


settings = importlib.import_module('MAC_SETTINGS')
category = '9355'
conn = utility.get_mongo_connection()
items = utility.get_collection(category, 'items', conn)



features_list = []
targets = []

for i in range(0, 1):
	center_html = items.find()[i]['html1']['CenterPanelInternal']
	descr_html = items.find()[i]['html1']['vi-desc-maincntr']
	center = tasks.parse_center(center_html)
	#descr = tasks.parse_descr(descr_html)

	s_rating = center['seller_rating']
	#s_percentage = center['seller_percentage']
	title = center['item_title']
	condition = center['condition']
	timestamp_end = center['timestamp_end']
	n_images = len(center['images'])

	sold = None
	if center['bids'] > 0:
		sold = 1
	elif center['bids'] <= 0:
		sold = 0


	features = [s_rating, condition, timestamp_end, n_images]
	target = sold
	features_list.append(features); targets.append(target)

print features_list
print targets

clf = MultinomialNB()
clf.fit(features_list, targets)


#code.interact(local=locals())



