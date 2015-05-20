import pymongo
from importlib import import_module
from utility import *
from bson import ObjectId
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
		self.deletion_filename = 'out%s.file' % self.category
		print 'Deletion file name is : %s' % self.deletion_filename


	def run_program(self):
		invalids = []

		#Load from deletion file all invalids
		with open(self.deletion_filename) as deletions:
			list_string = deletions.readlines()[0]
			l = list_string[2:len(list_string)-2].split('\', \'')

			#for item in l:
				#program.items_c.remove({"_id": ObjectId(item)})

			item = program.items_c.find({"_id" : ObjectId(l[0])})[0]

			_exception = False

			if 'item_id' not in item.keys() or 'html1' not in item.keys():
				_exception = True
			else:	
				item_id = item['item_id']
				html1 = item['html1']

			condition = _exception or (item_id is None) or (item_id == '') or (html1 is None) or (html1 == {}) or (html1 == '')
			print condition

			print len(l)



		#Loop through invalids and delete each one

		#for invalid in invalids:
		#	result = program.items.remove({"_id" : ObjectId(invalid)})
		#	if result['n'] != 1:
		#		print result


#Execute code here
program = Program()
program.run_program()