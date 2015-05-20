import pymongo
from bson import ObjectId
from tasks import *
import code

MONGO_IP = '146.169.47.50'
MONGO_PORT = '27017'

connection = pymongo.Connection('mongodb://%s:%s' % (MONGO_IP, MONGO_PORT), safe=True)

#Randomly load from the db n data points
def load_data(categories, bid_section, n):
	db = connection['auction_items']
	items = db._171957.find()
	dataset = []

	for i in range(0, n):
		center = parse_center(items[i]['html1']['CenterPanelInternal'])
		vals = center.values()
		_d = {'item_title': vals[0], 'seller_rating': vals[1], 'seller_percentage': vals[4], 'num_images': len(vals[5]), 'end_timestamp': vals[6], 'condition': vals[7]}
		dataset.append(_d)
	return dataset

dataset = load_data(None, None, 100)

code.interact(local=locals())