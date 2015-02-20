import pymongo
from importlib import import_module
from utility import *
import cherrypy
import json

settings = import_module(os.environ['SETTINGS'])

class Root(object):
	
	def __init__(self, program):
		super(Root, self).__init__()
		self.coll = program.collection

	@cherrypy.expose
	def index(self, entry_id);
		item = self.coll.find({'_id': entry_id})
		raw_html = item['raw_html']
		return raw_html

	@cherrypy.expose
	def count(self):
		return self.cursor.count().__str__()

class Program():
	
	def __init__(self):
		self.category = CATEGORY
		self.conn = get_mongo_connection()
		self.collection = get_collection(CATEGORY, 'items', self.conn)
		self.bfilter = get_filter(CATEGORY, 'items')

	def run_program(self):
		C_IP = '0.0.0.0'
		C_PORT = 443
		cherrypy.config.update({'server.socket_host': C_IP,
					'server.socket_port': C_PORT,
					})
		cherrypy.quickstart(Root(self))

program = Program()
program.run_program()


