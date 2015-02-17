import pymongo
from importlib import import_module
from utility import *
import cherrypy
import json

settings = import_module(os.environ['SETTINGS'])

class Root(object):
	
	def __init__(self, program):
		super(Root, self).__init__()
		self.cursor = program.collection.find()

	@cherrypy.expose
	def index(self, start, end):
		links = []
		start_num = int(start)
		end_num = int(end)

		for i in range(start_num, end_num + 1):
			item = self.cursor[i]
			item_id = item['item_id']
			link = item['link']
			n_item = {'item_id': item_id, 'link': link}
			links.append(n_item)
		return json.dumps(links)

	@cherrypy.expose
	def count(self):
		return self.cursor.count().__str__()

class Program():
	
	def __init__(self):
		self.category = CATEGORY
		self.conn = get_mongo_connection()
		self.collection = get_collection(CATEGORY, 'links', self.conn)
		self.bfilter = get_filter(CATEGORY, 'links')

	def run_program(self):
		C_IP = '0.0.0.0'
		C_PORT = 443
		cherrypy.config.update({'server.socket_host': C_IP,
					'server.socket_port': C_PORT,
					})
		cherrypy.quickstart(Root(self))

program = Program()
program.run_program()


