import pymongo
from importlib import import_module
from utility import *
import sys
import code

settings = import_module('MAC_SETTINGS')
category = sys.argv[1]
conn = get_mongo_connection()
items_c = get_collection(category, 'items', conn)

i = 0
num_bids = 0
items = items_c.find()

while True:
	if i >= items.count():
		break

	if 'bid_section' in items[i].keys():
		num_bids += 1	
	i += 1

print('Number of items : %s, Number of bid items : %s' % (i, num_bids))

