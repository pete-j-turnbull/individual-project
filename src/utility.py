from pybloomfilter import BloomFilter
import pymongo
import logging
import traceback
import os
from importlib import import_module

settings = import_module(os.environ['SETTINGS'])

def get_mongo_connection():
	try:
		conn = pymongo.Connection('mongodb://%s:%s' % (settings.MONGO_IP, settings.MONGO_PORT))
		logging.debug('Loaded mongo connection: %s' % conn)
		return conn
	except Exception as e:
		logging.error(e)
		return None

def get_collection(cat_num, collection, conn):
	try:
		if collection == 'links' or collection == 'items':
			db = conn['auction_%s' % collection]
			if cat_num == '9355':
				return db._9355
			if cat_num == '175672':
				return db._175672
			if cat_num == '171957':
				return db._171957
			if cat_num == '171485':
				return db._171485
			if cat_num == '15052':
				return db._15052
			if cat_num == '32852':
				return db._32852
			if cat_num == '50582':
				return db._50582
		logging.error('Return None for collection - category: %s, collection: %s' % (cat_num, collection))
		return None
	except Exception as e:
		logging.error(e)
		return None

def get_filter(cat_num, operation_name):
	try:
		filter_name = '%s/%s_%s.bloom' % (settings.BLOOM_DIR, operation_name, cat_num)
		logging.debug('Bloom filter file name: %s' % filter_name)
		if os.path.isfile(filter_name):
			bfilter = BloomFilter.open(filter_name)
		else:
			bfilter = BloomFilter(capacity=10000000, error_rate=0.0001, filter_name)
		return bfilter
	except Exception as e:
		logging.error(e)
		return None


def insert(collection, item):
	if settings.DEBUG:
		db = open(settings.FAKE_DATABASE, 'a')
		db.write('%s\n' % item.__str__())
	else:
		collection.insert(item)


