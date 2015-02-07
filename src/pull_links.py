from celery.execute import send_task
from pybloomfilter import BloomFilter
import pymongo
import time
import sys
from utility import *

category = sys.argv[1]
cat_num = int(category)
conn = get_mongo_connection()
collection = {'c': get_collection(cat_num, 'links', conn)}
bfilter = {'f': get_filter(cat_num, 'links')}


while True:
	try:
		page1 = send_task("tasks.scrape_page", ['https://api.import.io/store/data/c6001c48-1e16-4702-917d-83a623745a31/_query?input/webpage/url=http://www.ebay.com/sch/%s/i.html?LH_Auction=1&LH_Complete=1&rt=nc&_user=e09d4c84-e281-4a8a-a60d-f3d0c74ee59c&_apikey=mLo5A0Frb2Iq6lIa6XBjzeKhgxYXpNsfxwrJL3tb1QNlHxjwoJmkPVuf3HS5xlcirNZ0x06xlKJ38hggqzds/Q==' % cat_num])
		p1 = page1.get()
		for url in p1:
			item_id = url['item_id']
			link = url['link']
			if not bfilter['f'].add(item_id):
				insert(collection['c'], {'item_id': item_id, 'link': link})
	except Exception as e:
		print(e)

	time.sleep(15)
