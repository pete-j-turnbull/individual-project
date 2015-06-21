from ebay_loader import load_data

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

(training_set, testing_set) = load_data(9355, 6, 6)

CAT_SPACING = 20


titles = []
price_cats = []
for d in training_set:
	titles.append(d[0]['item_title'])
	price_cat = (d[1] - (d[1] % CAT_SPACING)) / CAT_SPACING
	price_cats.append(price_cat)


vectorizer = CountVectorizer(min_df=1)


_X = vectorizer.fit_transform(titles)

tf_transformer = TfidfTransformer()
X = tf_transformer.fit_transform(_X)

model = MultinomialNB().fit(X, price_cats)


#Now run the test data through the model
titles = []
for d in testing_set:
	titles.append(d[0]['item_title'])

X = tf_transformer.transform( vectorizer.transform(titles) )
prices_pred = map((lambda x: (x * CAT_SPACING) + CAT_SPACING / 2), model.predict(X))

for (title, price) in zip(titles, prices_pred):
	print '%s => $%s' % (title, price)



#Calc percentage error.
def _compare(test_set, predictions):
	error = 0
	total = 0
	for (t1, t2) in zip(test_set, predictions):
		diff = t1[1] - t2
		error += diff*diff
		total += t1[1]
	p = error / total
	return p





#Compare predictions against actual and print out the results
results = _compare(testing_set, prices_pred)
print results


