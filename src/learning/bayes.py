from ebay_loader import load_data

dataset = load_data(9355, False, 100)

for d in dataset:
	print d['condition']
