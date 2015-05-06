import pymongo
from importlib import import_module
from utility import *
import code

settings = import_module(os.environ['SETTINGS'])

#Return a list of mongo ids of items to be deleted as invalid.
#Item is invalid if one of the following hold:
#  - Empty bid_section
#  - Empty html1
#  - Empty item_id

class Program():

	def __init__(self):
		self.category = CATEGORY
		self.conn = get_mongo_connection()
		self.items_c = get_collection(CATEGORY, 'items', self.conn)



	def run_program(self):
		invalids = []

		i = 0
		items = self.items_c.find()
		while True:
			if i >= items.count():
				#Finished scanning
				break

			entry_id = items[i]['_id'].__str__()

			try:
				item_id = items[i]['item_id']
				html1 = items[i]['html1']
				bid_section = items[i]['bid_section']
			except:
				_exception = True

			condition = _exception or (item_id is None) or (item_id == '') or (html1 is None) or (html1 == {}) or (html1 == '') or (bid_section is None) or (bid_section == '') or (bid_section == {})

			if condition:
				invalids += entry_id
				print entry_id

			i += 1


#Execute code here
program = Program()
program.run_program()
code.interact(local=locals())