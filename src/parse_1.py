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
		self.bfilter = get_filter(CATEGORY, 'items_html1')

	def run_program(self):
		i = 0
		items = self.items_c.find()
		while True:
			if i >= items.count():
				break
			try:
				entry_id = items[i]['_id'].__str__()
				if not self.bfilter.add(entry_id):

					_obj = send_task("tasks.parse_item_1", [entry_id])
					obj = _obj.get()

					if not obj['success']:
						exception = obj['response']
						logging.error('Item parse 1 EntryID(%s) failed due to worker exception: %s' % (entry_id, exception))
						continue

					r = obj['result']
					logging.debug('Item parse 1 succeeded for item ID: %s, entry ID: %s' % (r['item_id'], entry_id))

					update(self.items_c, entry_id, {"item_id": r['item_id'], "html1": r['html1']} )

				i += 1
			except Exception as e:
				logging.error('Failed to parse item(1) for entry_id: %s' % entry_id, exc_info=True) 
				i += 1


#Execute code here
program = Program()
program.run_program()