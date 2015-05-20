import pymongo
from bson import ObjectId
import code

MONGO_IP = '146.169.47.50'
MONGO_PORT = '27017'

connection = pymongo.Connection('mongodb://%s:%s' % (MONGO_IP, MONGO_PORT), safe=True)

#Randomly load from the db n data points
def load(categories, bid_section, n):
	db = connection['auction_items']
	items = db._171957.find()
	loaded = []

	for i in range(0, items.count()):
		loaded.append(items[i]['item_id'])
	return loaded