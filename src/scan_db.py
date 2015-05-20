import pymongo
from importlib import import_module
from utility import *
import sys
import code

settings = import_module('ICLOUD_SETTINGS')
category = sys.argv[1]
conn = get_mongo_connection()
items_c = get_collection(category, 'items', conn)

#Return a list of mongo ids of items to be deleted as invalid.
#Item is invalid if one of the following hold:
#  - Empty bid_section
#  - Empty html1
#  - Empty item_id

invalids = []
i = 0
items = items_c.find()

while True:
	if i >= items.count():
		break

	entry_id = items[i]['_id'].__str__()
	_exception = False

	if 'item_id' not in items[i].keys() or 'html1' not in items[i].keys() or 'bid_section' not in items[i].keys():
		_exception = True
	else:	
		item_id = items[i]['item_id']
		html1 = items[i]['html1']
		bid_section = items[i]['bid_section']

	condition = _exception or (item_id is None) or (item_id == '') or (html1 is None) or (html1 == {}) or (html1 == '') or (bid_section is None) or (bid_section == '') or (bid_section == {})
	if condition:
		invalids.append(entry_id)

	print '%s : %s' % (category, i)
	i += 1

outfile = open('out%s.file' % category, 'w')
outfile.write('%s\n' % invalids.__str__())
outfile.close()

