import pymongo
from importlib import import_module
from utility import *
from bson import ObjectId
from json import load
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
			data = json.load(deletions)
			print data


		#Loop through invalids and delete each one

		#for invalid in invalids:
		#	result = program.items.remove({"_id" : ObjectId(invalid)})
		#	if result['n'] != 1:
		#		print result


#Execute code here
program = Program()
program.run_program()