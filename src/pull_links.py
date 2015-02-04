from celery.execute import send_task
from pybloomfilter import BloomFilter
import pymongo
import time
import sys

alinksname = sys.argv[1]

conn = pymongo.Connection('mongodb://10.240.113.54:27017')
links = {'l': None}
bfilter = {'f': None}
cat_num = int(alinksname)

if cat_num == 9355:
	links['l'] = conn['auction_links']._9355
	bfilter['f'] = BloomFilter.open('./bloomfilters/links_9355.bloom')
elif cat_num == 175672:
	links['l'] = conn['auction_links']._175672
	bfilter['f'] = BloomFilter.open('./bloomfilters/links_175672.bloom')
elif cat_num == 171957:
	links['l'] = conn['auction_links']._171957
	bfilter['f'] = BloomFilter.open('./bloomfilters/links_171957.bloom')
elif cat_num == 171485:
	links['l'] = conn['auction_links']._171485
	bfilter['f'] = BloomFilter.open('./bloomfilters/links_171485.bloom')
elif cat_num == 15052:
	links['l'] = conn['auction_links']._15052
	bfilter['f'] = BloomFilter.open('./bloomfilters/links_15052.bloom')
elif cat_num == 32852:
	links['l'] = conn['auction_links']._32852
	bfilter['f'] = BloomFilter.open('./bloomfilters/links_32852.bloom')
elif cat_num == 50582:
	links['l'] = conn['auction_links']._50582
	bfilter['f'] = BloomFilter.open('./bloomfilters/links_50582.bloom')


while True:
	try:
		page1 = send_task("tasks.scrape_page", ['https://api.import.io/store/data/c6001c48-1e16-4702-917d-83a623745a31/_query?input/webpage/url=http://www.ebay.com/sch/%s/i.html?LH_Auction=1&LH_Complete=1&rt=nc&_user=e09d4c84-e281-4a8a-a60d-f3d0c74ee59c&_apikey=mLo5A0Frb2Iq6lIa6XBjzeKhgxYXpNsfxwrJL3tb1QNlHxjwoJmkPVuf3HS5xlcirNZ0x06xlKJ38hggqzds/Q==' % cat_num])
		p1 = page1.get()
		for url in p1:
			item_id = url['item_id']
			link = url['link']
			if not bfilter['f'].add(item_id):
				links['l'].insert( {'item_id': item_id, 'link': link} )
	except:
		pass

	time.sleep(15)
