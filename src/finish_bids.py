import pymongo
from importlib import import_module
from utility import *
from bson import ObjectId
import code

settings = import_module(os.environ['SETTINGS'])

#Go through entries looking for those without bid_section and add it.

class Program():

	def __init__(self):
		self.category = CATEGORY
		self.conn = get_mongo_connection()
		self.items_c = get_collection(CATEGORY, 'items', self.conn)


	def run_program(self):
		cursor = self.items_c.find()
		i = 0
		for i in range(0, cursor.count()):
			item = cursor[i]
			if item['bid_section'] is None:
				print 'No bid section at item: %s' % item['item_id']



#Execute code here
program = Program()
program.run_program()