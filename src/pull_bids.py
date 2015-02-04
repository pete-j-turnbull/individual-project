from pybloomfilter import BloomFilter
from requests import get
from celery.execute import send_task
import pymongo
import time
import sys
import re

alinksname = sys.argv[1]

conn = pymongo.Connection('mongodb://10.240.113.54:27017')
items = {'i': None}
bfilter = {'f': None}
cat_num = int(alinksname)

if cat_num == 9355:
        items['i'] = conn['auction_items']._9355
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_bid_9355.bloom')
elif cat_num == 175672:
        items['i'] = conn['auction_items']._175672
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_bid_175672.bloom')
elif cat_num == 171957:
        items['i'] = conn['auction_items']._171957
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_bid_171957.bloom')
elif cat_num == 171485:
        items['i'] = conn['auction_items']._171485
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_bid_171485.bloom')
elif cat_num == 15052:
        items['i'] = conn['auction_items']._15052
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_bid_15052.bloom')
elif cat_num == 32852:
        items['i'] = conn['auction_items']._32852
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_bid_32852.bloom')
elif cat_num == 50582:
        items['i'] = conn['auction_items']._50582
        bfilter['f'] = BloomFilter.open('./bloomfilters/items_bid_50582.bloom')

i = 0
its = items['i'].find()
while True:
	if i >= its.count():
		break
	try:
		item_url = its[i]['pageUrl']
		m = re.search('ebay.com/itm/([0-9]+)\?', item_url)
		item_id = m.group(1)

		if not bfilter['f'].add(item_id):
			doc_id = its[i]['_id']

			bids_url = its[i]['results'][0]['bids_link']
			_bids_json = send_task("tasks.scrape_bids", ['https://api.import.io/store/data/d71a71f5-d4e7-42a3-8d58-6ae70b6e4a3e/_query?input/webpage/url=http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids%26item%3D' + item_id + '%26rt%3Dnc%26_trksid%3Dp2047675.l2565&_user=e09d4c84-e281-4a8a-a60d-f3d0c74ee59c&_apikey=mLo5A0Frb2Iq6lIa6XBjzeKhgxYXpNsfxwrJL3tb1QNlHxjwoJmkPVuf3HS5xlcirNZ0x06xlKJ38hggqzds%2FQ%3D%3D'])
			bids_json = _bids_json.get()

			bid_results = bids_json['results']

			itm = items['i'].find_one({"_id": doc_id})
			itm['bid_section'] = bid_results
			items['i'].save(itm)
	except:
		pass

	i += 1
