import pymongo
from importlib import import_module
from utility import *
import code

settings = import_module(os.environ['SETTINGS'])

class Program():

	def __init__(self):
		self.category = CATEGORY
		self.conn = get_mongo_connection()
		self.collection = get_collection(CATEGORY, 'items', self.conn)
		self.bfilter = get_filter(CATEGORY, 'items')


#Execute code here
program = Program()
code.interact(local=locals())
