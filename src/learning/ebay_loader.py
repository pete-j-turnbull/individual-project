import sys
sys.path.append('../')

import pymongo
from bson import ObjectId
from tasks import *

MONGO_IP = '146.169.47.50'
MONGO_PORT = '27017'
''
#connection = pymongo.Connection('mongodb://%s:%s' % (MONGO_IP, MONGO_PORT), safe=True)

data = [({'item_title': 'Apple iPhone 5 - 32GB - Black &amp; Slate (AT&amp;T) Smartphone'}, 207.50), ({'item_title': 'Apple iPhone 6 (Latest Model) - 16GB - Silver (AT&amp;T) Smartphone'}, 590.0), ({'item_title': 'Apple iPhone 5 - 16GB - Black &amp; Slate (AT&amp;T) Smartphone'}, 67.0), ({'item_title': 'Apple iPhone 3G (8 GB) UNLOCKED'}, 39.99), 
		({'item_title': 'Apple iPhone 5c - 32GB - Pink (AT&amp;T) Smartphone'}, 242.50), ({'item_title': 'Samsung Galaxy S5 Active SM-G870A (Latest Model) - 16GB - Camo Green (AT&amp;T)...'}, 455.0), ({'item_title': 'Apple iPhone 5s - 16GB - Space Gray (Verizon) Smartphone'}, 255.0), ({'item_title': 'Apple iPhone 4 - 8GB - Black (AT&amp;T) Smartphone (MD126LL/A)'}, 49.0), 
		({'item_title': 'Apple iPhone 5 - 32GB - White &amp; Silver (AT&amp;T) Smartphone'}, 192.50), ({'item_title': 'Apple iPhone 5 - 16GB - Black &amp; Slate (Verizon) Smartphone'}, 200.0), ({'item_title': 'Apple iPhone 5c - 16GB - Blue (T-Mobile) Smartphone'}, 173.50), ({'item_title': 'Apple iPhone 4S (16GB) Black VERIZON Smartphone C'}, 79.91)]


#Randomly load from the db n data points
def load_data(category, n_train, n_test):
	#db = connection['auction_items']
	#items = None

	#if category == 9355:
	#	items = db._9355.find()
	#elif category == 175672:
	#	items = db._175672.find()
	#elif category == 171957:
	#	items = db._171957.find()
	#elif category == 171485:
	#	items = db._171485.find()
	#elif category == 15052:
	#	items = db._15052.find()
	#elif category == 32852:
	#	items = db._32852.find()
	#elif category == 50582:
	#	items = db._50582.find()

	training_set = []
	testing_set = []

	for i in range(0, n_train):
		try:
			#center = parse_center(items[i]['html1']['CenterPanelInternal'])
			#vals = center.values()
			#d1 = {'item_title': vals[0], 'seller_rating': vals[2], 'seller_percentage': vals[5], 'num_images': len(vals[6]), 'end_timestamp': vals[7], 'condition': vals[8]}
			#d2 = vals[1]
			training_set.append(data[i])
		except Exception as e:
			print i

	for i in range(n_train, n_train + n_test):
		try:
			#center = parse_center(items[i]['html1']['CenterPanelInternal'])
			#vals = center.values()
			#d1 = {'item_title': vals[0], 'seller_rating': vals[2], 'seller_percentage': vals[5], 'num_images': len(vals[6]), 'end_timestamp': vals[7], 'condition': vals[8]}
			#d2 = vals[1]
			testing_set.append(data[i])
		except Exception as e:
			print i


	return (straining_set, testing_set)
