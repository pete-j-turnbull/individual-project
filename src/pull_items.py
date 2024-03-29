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
		self.links_c = get_collection(CATEGORY, 'links', self.conn)
		self.items_c = get_collection(CATEGORY, 'items', self.conn)
		self.bfilter = get_filter(CATEGORY, 'items_raw')
		self.efilter = get_filter(CATEGORY, 'items_raw_error')

	def run_program(self):
		i = int(START_INDEX)
		ls = self.links_c.find()
		code.interact(local=locals())
		while True:
			if i >= ls.count():
				break
			try:
				item_id = ls[i]['item_id']
				if not self.bfilter.add(item_id):
					_p = send_task("tasks.scrape_item", ['http://www.ebay.com/itm/%s?orig_cvip=true' % item_id])
					p = _p.get()

					#Do error checking here - insert ERROR and continue if there is a problem
					if not p['success']:
						r = p['response']
						if p['exception']:
							logging.error('Item scrape ID(%s) failed due to worker exception: %s' % (item_id, r))
							continue
						else:
							logging.error('Item scrape ID(%s) failed with code: %s, reason: %s, response_text: %s for item: %s' 
								% (item_id, r.status_code, r.reason, r.text, item_id))
							self.efilter.add(item_id)
							continue

					r = p['response']
					logging.debug('Item scrape succeeded with code: %s for url: %s' 
						% (r.status_code, r.url))

					item = {'raw_html': r.text}
					insert(self.items_c, item)
				i += 1
			except Exception as e:
				logging.error('Failed to scrape item for item_id: %s' % item_id, exc_info=True)
				self.efilter.add(item_id)
				i += 1


#Execute code here
program = Program()
program.run_program()

