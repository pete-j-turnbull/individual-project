import pymongo
from importlib import import_module
from utility import *
from bson import ObjectId
from tasks import *
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
			if not 'bid_section' in item.keys():
				#Get bid section
				bids_url = 'http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids&item=%s&showauto=true' % item['item_id']
				obj = get_bids(bids_url)

				success = obj['success']
				if success:
					bid_section = obj['result']
					print 'Success : %s, bid_section : %s' % (success, bid_section)
				else:
					print 'Failed for item : %s' % item['item_id']



#Execute code here
program = Program()
program.run_program()