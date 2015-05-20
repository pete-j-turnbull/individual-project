from celery.task import task
from requests import get
import re
import json
from bs4 import BeautifulSoup
from datetime import *
import code

#Utility methods
def month_conv(month):
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	try:
		return months.index(month) + 1
	except ValueError:
		return -1

def getdatetime(datestring):
	st = re.search('([A-Za-z]*)-([0-9]*)-([0-9]*)\s*([0-9]*):([0-9]*):([0-9]*)', datestring)
	t = datetime(int('20'+st.group(3)), month_conv(st.group(1)), int(st.group(2)), int(st.group(4)), int(st.group(5)), int(st.group(6)))
	return t

def getepoch(dt):
	return (dt - datetime(1970,1,1)).total_seconds()

def conv_duration(d_text):
	days = re.search('([0-9]*)\s*day', d_text).group(1)
	duration = int(days) * 24 * 3600
	return duration


def e_with_classes(soup, element_type, classes):
	elems = []
	if classes == []:
		return soup(element_type)

	for elem in soup(element_type):
		_classes = elem.get('class')
		if _classes is None:
			continue
		else:
			for _class in _classes:
				if _class in classes:
					elems.append(elem)
	return elems

def e_with_ids(soup, element_type, ids):
	elems = []
	if ids == []:
		return soup(element_type)

	for elem in soup(element_type):
		_id = elem.get('id')
		if _id is None:
			continue
		else:
			if _id in ids:
				elems.append(elem)
	return elems




#Actual tasks here
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
			return {'success': False, 'response': resp, 'exception': False}
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
def parse_center(center):
	soup = BeautifulSoup(center)
	item = {}

	sellerinfo = e_with_classes(soup, 'div', ['si-inner'])[0]
	item['seller_rating'] = e_with_ids(sellerinfo, 'a', [])[1].text

	_sdf = e_with_ids(sellerinfo, 'div', ['si-fb'])
	if _sdf == []:
		pass
	else:
		item['seller_percentage'] = re.search('([0-9.]*)', _sdf[0].text).group(1)

	item['item_title'] = re.search('span>(.*)</h1>', e_with_ids(soup, 'h1', ['itemTitle'])[0].__str__()).group(1)


	#image urls
	picture_panel = e_with_classes(soup, 'div', ['pp-ic', 'pp-ic500'])[0]

	_pic_slider = e_with_ids(picture_panel, 'div', ['vi_main_img_fs_slider'])
	if _pic_slider == []:
		item['images'] = []
	else:
		pic_slider = _pic_slider[0]
		images = []
		for image in e_with_ids(pic_slider, 'img', []):
			images.append(re.search('src=\"(.*)\" style', image.__str__()).group(1))
		item['images'] = images


	p1 = e_with_classes(soup, 'div', ['nonActPanel'])[0]
	p2 = e_with_classes(soup, 'div', ['actPanel'])[0]
	_time = e_with_classes(p1, 'span', ['endedDate'])[0]

	item['condition'] = e_with_ids(p1, 'div', ['vi-itm-cond'])[0].text
	item['timestamp_end'] = re.search('timems=\"([0-9]*)\">', _time.__str__()).group(1)

	item['delivery'] = e_with_classes(soup, 'div', ['sh-del-frst']).__str__()
	item['payments'] = e_with_ids(soup, 'div', ['payDet1']).__str__()
	item['returns'] = e_with_ids(soup, 'span', ['vi-ret-accrd-txt']).__str__()

	return item


@task
def parse_descr(descr):
	soup = BeautifulSoup(descr)
	item = {}

	item['specifics'] = e_with_classes(soup, 'div', ['section']).__str__()
	item['extra'] = e_with_ids(soup, 'div', ['desc_div'])
	item['qanda'] = e_with_classes(soup, 'div', ['asqContent']).__str__()

	return item


@task
def get_bids(url):
	try:
		resp = get(url)
		if resp.status_code != 200:
			return {'success': False, 'response': resp, 'exception': False}

		raw_html = resp.text
		soup = BeautifulSoup(raw_html)
		bids_item = {}

		xs = e_with_classes(soup, 'div', ['BHbidSecBorderGrey'])
		top = xs[0]
		bottom = xs[1]
		ys = e_with_classes(bottom, 'span', ['titleValueFont'])

		bids_item['numbidders'] = ys[0].text
		bids_item['numbids'] = ys[1].text
		bids_item['duration'] = conv_duration(ys[3].text)

		te = getdatetime(ys[2].text)
		bids_item['end_time'] = te.__str__()
		bids_item['end_timestamp'] = getepoch(te)
		bids_item['final_price'] = re.search('\$(.*\..*)', e_with_classes(top, 'td', ['BHctBidVal'])[0].text).group(1)

		#Bids table
		bt = e_with_ids(bottom, 'div', ['vizrefdiv'])[0]
		bids_table = e_with_classes(bt, 'td', ['contentValueFont', 'newcontentValueFont', 'onheadNav'])

		#Check if bids table is empty - means 0 bids placed
		if len(bids_table) == 0:
			bids_item['numbidsauto'] = 0
			bids_item['starting_price'] = bids_item['final_price']
			bids_item['start_timestamp'] = bids_item['end_timestamp'] - bids_item['duration']
			bids_item['start_time'] = datetime.fromtimestamp(bids_item['start_timestamp']).__str__()
		else:
			bids_item['numbidsauto'] = (len(bids_table) / 3) - 1
			bids_item['starting_price'] = re.search('\$(.*\..*)', bids_table[len(bids_table)-2].text).group(1)
			ts = getdatetime(bids_table[len(bids_table)-1].text)
			bids_item['start_time'] = ts.__str__()
			bids_item['start_timestamp'] = getepoch(ts)

		#Parse bids table
		bids = []
		if len(bids_table) == 0:
			pass
		else:
			for i in range(0, len(bids_table)-3, 3):
				_bidder = bids_table[i]
				auto = False
				if _bidder.get('class')[0] == 'newcontentValueFont':
					auto = True

				bid = re.search('\$(.*\..*)', bids_table[i+1].text).group(1)
				btime = getdatetime(bids_table[i+2].text)
				bid_time = btime.__str__()
				bid_timestamp = getepoch(btime)
				bids.append({'bid':bid, 'bid_time':bid_time, 'bid_timestamp':bid_timestamp, 'auto':auto})
		bids_item['bids'] = bids
		return {'success': True, 'result': bids_item}
	except Exception as e:
		return {'success': False, 'response': e, 'exception': True}

