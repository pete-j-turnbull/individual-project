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

	def run_program(self):
		i = 0
		try:
			its = self.items_c.find()
			while True:
				if i >= its.count():
					break
				try:
					item_url = its[i]['pageUrl']
					m = re.search('ebay.com/itm/([0-9]+)\?', item_url)
					item_id = m.group(1)

					if not self.bfilter.add(item_id):
						bids_url = its[i]['results'][0]['bids_link']
						_b = send_task("tasks.scrape_bids", ['https://api.import.io/store/data/d71a71f5-d4e7-42a3-8d58-6ae70b6e4a3e/_query?input/webpage/url=http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids%26item%3D' + item_id + '%26rt%3Dnc%26_trksid%3Dp2047675.l2565&_user=e09d4c84-e281-4a8a-a60d-f3d0c74ee59c&_apikey=mLo5A0Frb2Iq6lIa6XBjzeKhgxYXpNsfxwrJL3tb1QNlHxjwoJmkPVuf3HS5xlcirNZ0x06xlKJ38hggqzds%2FQ%3D%3D'])
						b = _b.get()
						if not b['success']:
							r = b['response']
	        				logging.error('Bid scrape failed with code: %s, reason: %s, response_text: %s for item: %s' 
								% (r.status_code, r.reason, r.text, item_id))
	        			r = b['response']
	        			logging.debug('Bid scrape sudceeded with code: %s for item: %s'
	        				% (r.status_code, item_id))

	        			bids = b['result']
	        			its[i]['bid_section'] = bids
	        			self.items_c.save(its[i])
				except Exception as e:
					logging.error('Failed to scrape bids for item_id: %s' % item_id, exc_info=True) 
				i += 1

		except Exception as e:
			logging.error('Failed to scrape any bids', exc_info=True) 


#Execute code here
program = Program()
program.run_program()
