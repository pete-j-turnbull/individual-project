from celery.execute import send_task
from pybloomfilter import BloomFilter
import pymongo
import time
import os
from importlib import import_module
from utility import *
import code

settings = import_module(os.environ['SETTINGS'])


class Program():

	def __init__(self):
		self.category = CATEGORY
		self.conn = get_mongo_connection()
		self.items_c = get_collection(CATEGORY, 'items', self.conn)
		self.bfilter = get_filter(CATEGORY, 'bids')

		self.bfilter = get_filter(CATEGORY, 'bids')
		self.efilter = get_filter(CATEGORY, 'bids_error')

	def run_program(self):
		i = int(START_INDEX)
		items = self.items_c.find()
		while True:
			if i >= items.count():
				break
			entry_id = items[i]['_id'].__str__()
			try:
				item_id = items[i]['item_id']
				if not self.bfilter.add(item_id):
					bids_url = 'http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids&item=%s&showauto=true' % item_id
					_obj = send_task("tasks.get_bids", [bids_url])
					obj = _obj.get()

					if not obj['success']:
						exception = obj['response']
						logging.error('Bid scrape failed for entryID: %s (itemID:%s) in category: %s due to worker exception: %s' 
							% (entry_id, item_id, self.category, exception))
						self.efilter.add(entry_id)
						i += 1
						continue

					logging.debug('Bid scrape succeeded for item: %s' % item_id)
					bids = obj['result']
					update(self.items_c, items[i]['_id'], {"bid_section": bids}, {})

			except Exception as e:
				logging.error('Failed to scrape bids for entryID: %s in category: %s' % (entry_id, self.category), exc_info=True)
				self.efilter.add(entry_id)

			i += 1


#Execute code here
program = Program()
program.run_program()
