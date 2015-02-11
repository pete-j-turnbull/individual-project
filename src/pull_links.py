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
		self.collection = get_collection(CATEGORY, 'links', self.conn)
		self.bfilter = get_filter(CATEGORY, 'links')

	def run_program(self):
		while True:
			try:
				page1 = send_task("tasks.scrape_page", ['https://api.import.io/store/data/c6001c48-1e16-4702-917d-83a623745a31/' + 
					'_query?input/webpage/url=http://www.ebay.com/sch/%s/i.html?LH_Auction=1&LH_Complete=1&rt=nc&_user=e09d4c84-e281-4a8a-a60d-f3d0c74ee59c&_apikey=mLo5A0Frb2Iq6lIa6XBjzeKhgxYXpNsfxwrJL3tb1QNlHxjwoJmkPVuf3HS5xlcirNZ0x06xlKJ38hggqzds/Q==' % self.category])	
				p1 = page1.get()
				if not p1['success']:
					r = p1['response']
					logging.error('Page request failed with code: %s, reason: %s, response_text: %s for url: %s' 
						% (r.status_code, r.reason, r.text, r.url))
				r = p1['response']
				logging.debug('Page request succeeded with code %s for url: %s' 
						% (r.status_code, r.url))

				code.interact(local=locals())

				for url in p1['result']:
					item_id = url['item_id']
					link = url['link']
					if not self.bfilter.add(item_id):
						insert(self.collection, {'item_id': item_id, 'link': link})
			except Exception as e:
				logging.error('Failed to add links for category: %s' % self.category, exc_info=True) 

			time.sleep(15)


#Execute code here
program = Program()
program.run_program()

