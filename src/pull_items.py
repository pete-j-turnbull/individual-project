from pybloomfilter import BloomFilter
from celery.execute import send_task
import pymongo
import time
import sys

alinksname = sys.argv[1]

conn = pymongo.Connection('mongodb://10.240.113.54:27017')
links = {'l': None}
items = {'i': None}
bfilter = {'f': None}
cat_num = int(alinksname)

if cat_num == 9355:
        links['l'] = conn['auction_links']._9355
        items['i'] = conn['auction_items']._9355
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_9355.bloom')
elif cat_num == 175672:
        links['l'] = conn['auction_links']._175672
        items['i'] = conn['auction_items']._175672
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_175672.bloom')
elif cat_num == 171957:
        links['l'] = conn['auction_links']._171957
        items['i'] = conn['auction_items']._171957
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_171957.bloom')
elif cat_num == 171485:
        links['l'] = conn['auction_links']._171485
        items['i'] = conn['auction_items']._171485
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_171485.bloom')
elif cat_num == 15052:
        links['l'] = conn['auction_links']._15052
        items['i'] = conn['auction_items']._15052
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_15052.bloom')
elif cat_num == 32852:
        links['l'] = conn['auction_links']._32852
        items['i'] = conn['auction_items']._32852
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_32852.bloom')
elif cat_num == 50582:
        links['l'] = conn['auction_links']._50582
        items['i'] = conn['auction_items']._50582
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_50582.bloom')
 

i = 0
ls = links['l'].find()
while True:
 	if i >= ls.count():
 		break
 	try:
 		item_id = ls[i]['item_id']
 		if not bfilter['f'].add(item_id):
 			_item_json = send_task("tasks.scrape_item", ['https://api.import.io/store/data/0ab16a00-a230-4187-aa3b-e20e4f408980/_query?input/webpage/url=http://www.ebay.com/itm/%s?orig_cvip=true&_user=e09d4c84-e281-4a8a-a60d-f3d0c74ee59c&_apikey=mLo5A0Frb2Iq6lIa6XBjzeKhgxYXpNsfxwrJL3tb1QNlHxjwoJmkPVuf3HS5xlcirNZ0x06xlKJ38hggqzds/Q==' % item_id])
 			item_json = _item_json.get()
 			items['i'].insert(item_json)
 	except:
 		pass
 	i += 1
