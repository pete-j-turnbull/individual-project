from ebay_loader import load_data

dataset = load_data(9355, False, 200)

for d in dataset:
	print '%s : %s' % (d['item_title'], d['price'])
