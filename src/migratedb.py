import pymongo
from importlib import import_module
from utility import *
from requests import get
import json
import code

settings = import_module(os.environ['SETTINGS'])

class Program():

	def __init__(self):
		self.category = CATEGORY
		self.conn = get_mongo_connection()
		self.collection = get_collection(CATEGORY, 'links', self.conn)
		self.bfilter = get_filter(CATEGORY, 'links')


	def run_program(self):
		C_IP = '192.158.28.85'
		C_PORT = '443'

		#Get 2000 links at a time starting at index 0
		start = 0
		end = 1999
		last_iteration = False
		while True:
			count = int(get('http://%s:%s/count' % (C_IP, C_PORT)).text)
			if end > count - 1:
				end = count - 1
				last_iteration = True
			response = get('http://%s:%s?start=%s&end=%s' % (C_IP, C_PORT, start, end))
			json_resp = json.loads(response.text)

			for item in json_resp:
				#Add the item to the db
				insert(self.collection, item)

			if last_iteration:
				break
			start += 2000
			end += 2000


#Execute code here
program = Program()
program.run_program()

#Simple http server which exposes an endpoint whereby the database is accessed between index points a and b
#python manage.py expose_http --settings=GCLOUD_SETTINGS_DEBUG --category=9355