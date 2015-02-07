from celery.task import task
from requests import get
import re

@task
def scrape_page(url):
	urls = []

	resp = get(url)
	resp_j = resp.json()
	results = resp_j['results']

	for result in results:
		link = result['auto_column_3']
		m = re.search('ebay.com/itm/.*/([0-9]+)\?', link)
		item_id = m.group(1)
		urls.append({'item_id': item_id, 'link': link})

	return urls

@task
def scrape_item(url):
	resp = get(url)
	try:
		resp_j = resp.json()
		return resp_j
	except:
		return -1


@task
def scrape_bids(url):
	resp = get(url)
	try:
		resp_j = resp.json()
		return resp_j
	except:
		return -1
