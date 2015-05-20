import sys
sys.path.append('/home/guest/Development/individual_project/src')

import pymongo
from bson import ObjectId
from tasks import *

MONGO_IP = '146.169.47.50'
MONGO_PORT = '27017'

connection = pymongo.Connection('mongodb://%s:%s' % (MONGO_IP, MONGO_PORT), safe=True)

#Randomly load from the db n data points
def load_data(category, bid_section, n):
	db = connection['auction_items']
	items = None

	if category == 9355:
		items = db._9355.find()
	elif category == 175672:
		items = db._175672.find()
	elif category == 171957:
		items = db._171957.find()
	elif category == 171485:
		items = db._171485.find()
	elif category == 15052:
		items = db._15052.find()
	elif category == 32852:
		items = db._32852.find()
	elif category == 50582:
		items = db._50582.find()

	dataset = []

	for i in range(0, n):
		try:
			center = parse_center(items[i]['html1']['CenterPanelInternal'])
			vals = center.values()
			_d = {'item_title': vals[0], 'seller_rating': vals[1], 'seller_percentage': vals[4], 'num_images': len(vals[5]), 'end_timestamp': vals[6], 'condition': vals[7]}
			dataset.append(_d)
		except Exception as e:
			print i
	return dataset

