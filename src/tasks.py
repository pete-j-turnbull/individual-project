from celery.task import task
from requests import get
import re
import json
from bs4 import BeautifulSoup

@task
def scrape_page(url):
	urls = []

	try:
		resp = get(url)
		print(resp)
		if resp.status_code != 200:
			return {'success': False, 'response': resp, 'exception': False}
		resp_j = resp.json()
		results = resp_j['results']

		for result in results:
			link = result['auto_column_3']
			m = re.search('ebay.com/itm/.*/([0-9]+)\?', link)
			item_id = m.group(1)
			urls.append({'item_id': item_id, 'link': link})

		return {'success': True, 'response': resp, 'result': urls}
	except Exception as e:
		return {'success': False, 'response': e, 'exception': True}


@task
def scrape_item(url):
	try:
		resp = get(url)
		if resp.status_code != 200:
			return {'success': False, 'response': resp, 'exception': True}
		return {'success': True, 'response': resp}
	except Exception as e:
		return {'success': False, 'response': e, 'exception': True}


@task
def parse_item_1(raw_html):
	try:
		soup = BeautifulSoup(raw_html)
		divIds = ['CenterPanelInternal', 'shipNHadling', 'rpdId', 'payId', 'vi-desc-maincntr']
		obj = {'html1': {}, 'item_id': None}

		for d in soup.find_all('div'):

			div_class = d.get('class')
			div_id = d.get('id')
			if div_id in divIds:
				obj['html1'][div_id] = d.__str__()

			if div_class is None:
				continue
			elif 'iti-act-num' in div_class:
				id_text = d.__str__()
				m = re.search('>([0-9]+)</div>', id_text)
				obj['item_id'] = m.group(1)

		return {'success': True, 'result': obj}
	except Exception as e:
		return {'success': False, 'response': e, 'exception': True}


@task
def scrape_bids(url):
	try:
		resp = get(url)
		if resp.status_code != 200:
			return {'success': False, 'response': resp}
		resp_j = resp.json()
		return {'success': True, 'response': resp, 'result': resp_j}
	except Exception as e:
		return {'success': False, 'response': e}



