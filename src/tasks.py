from celery.task import task
from requests import get
import re
import json

@task
def scrape_page(url):
	urls = []

	try:
		resp = get(url)
		print(resp)
		if resp.status_code != 200:
			return {'success': False, 'response': resp}
		resp_j = resp.json()
		results = resp_j['results']

		for result in results:
			link = result['auto_column_3']
			m = re.search('ebay.com/itm/.*/([0-9]+)\?', link)
			item_id = m.group(1)
			urls.append({'item_id': item_id, 'link': link})

		return {'success': True, 'response': resp, 'result': urls}
	except Exception as e:
		return {'success': False, 'response': e}


@task
def scrape_item(url):
	try:
		resp = get(url)
		if resp.status_code != 200:
			return {'success': False, 'response': resp}
		resp_j = resp.json()
		return {'success': True, 'response': resp}
	except Exception as e:
		return {'success': False, 'result': e}


@task
def scrape_bids(url):
	try:
		resp = get(url)
		if resp.status_code != 200:
			return {'success': False, 'response': resp}
		resp_j = resp.json()
		return {'success': True, 'response': resp, 'result': resp_j}
	except Exception as e:
		return {'success': False, 'result': e}


