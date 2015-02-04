from pybloomfilter import BloomFilter
import pymongo
import re

conn = pymongo.Connection('mongodb://10.240.113.54:27017')
links = conn['auction_links']._50582
bfilter = BloomFilter.open('./bloomfilters/links_50582.bloom')
urls = open('./url_files/urls_50582.file', 'r')

for url in urls:
	m = re.search('ebay.com/itm/.*/([0-9]+)\?', url)
	if m is not None:
		item_id = m.group(1)
		if not bfilter.add(item_id):
			links.insert({'item_id': item_id, 'link': url})
