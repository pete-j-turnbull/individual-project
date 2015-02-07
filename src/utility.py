from pybloomfilter import BloomFilter
import pymongo
from settings import *

def get_mongo_connection():
	try:
		conn = pymongo.Connection('mongodb://%s:%s' % (MONGO_IP, MONGO_PORT))
		return conn
	except:
		return None

def get_collection(cat_num, collection_name, conn):
	try:
		if collection_name == 'links' or collection == 'items':
			db = conn['auction_%s' % collection_name]
			if cat_num == 9355:
				return db._9355
			if cat_num == 175672:
				return db._175672
			if cat_num == 171957:
				return db._171957
			if cat_num == 171485:
				return db._171485
			if cat_num == 15052:
				return db._15052
			if cat_num == 32852:
				return db._32852
			if cat_num == 50582:
				return db._50582
		return None
	except:
		return None

def get_filter(cat_num, collection):
	try:
		if collection == 'links' or collection == 'items' or collection == 'bids':
			bfilter = BloomFilter.open('%s/%s_%s.bloom' % (BLOOM_DIR, collection, cat_num))
			return bfilter
		return None
	except:
		return None


def insert(collection, item):
	if DEBUG:
		print("HERE")
		db = open(FAKE_DATABASE, 'a')
		db.write('%s\n' % item.__str__())
	else:
		collection.insert(item)

