#Import directory above tests
import sys
import os
import re
import importlib
sys.path.append('../')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import ward, dendrogram

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import nltk
import re
import mpld3
from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics.pairwise import cosine_similarity

import tasks
import utility
import pymongo
import code


def strip_tags(html):
    soup = BeautifulSoup(html)

    for tag in soup.findAll(True):
        tag.replaceWithChildren()
    return soup


def split_data(X, y, slices):
    '''
    Splits the data into training, validation and test sets.
    slices - relative sizes of each set (training, validation, test)
        test - provide None, since it is computed automatically
    '''
    datasets = {}
    starts = np.floor(np.cumsum(len(X) * np.hstack([0, slices[:-1]])))
    slices = {
        'training': slice(starts[0], starts[1]),
        'validation': slice(starts[1], starts[2]),
        'test': slice(starts[2], None)}
    data = X, y
    def slice_data(data, sl):
        return tuple(d[sl] for d in data)
    for label in slices:
        datasets[label] = slice_data(data, slices[label])
    return datasets


def get_items(items):
	ids = []
	titles = []
	ds = []
	prices = []
	for i in range(0, 4000):
		_id = items.find()[i]['item_id']
		center_html = items.find()[i]['html1']['CenterPanelInternal']
		center = tasks.parse_center(center_html)
		title = center['item_title']
		if center['price'] == None:
			continue
		_price = re.search('US \$(.*)', center['price'])
		if _price == None:
			continue
		price = float(_price.group(1).replace(',', ''))

		descr_html = items.find()[i]['html1']['vi-desc-maincntr']
		descr = tasks.parse_descr(descr_html)

		ids.append(_id)
		titles.append(title)
		ds.append(strip_tags(descr['specifics']).__str__().decode('utf-8'))
		prices.append(price)
	return ids, titles, ds, prices


def tfidf_descrs(descrs):
	vectorizer = CountVectorizer(min_df=1)
	_ds = vectorizer.fit_transform(descrs)
	tf_transformer = TfidfTransformer()
	ds_tf = tf_transformer.fit_transform(_ds)
	return ds_tf


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


settings = importlib.import_module('MAC_SETTINGS')
category = '9355'
conn = utility.get_mongo_connection()
item_coll = utility.get_collection(category, 'items', conn)

ids, titles, ds, prices = get_items(item_coll)


stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")


totalvocab_stemmed = []
totalvocab_tokenized = []
for i in ds:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print 'there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame'


ds_tfidf = tfidf_descrs(ds)




#KMEANS here
km = KMeans(n_clusters=7, init='k-means++', max_iter=100, n_init=1, verbose=True)
km.fit(ds_tfidf)
clusters = km.labels_.tolist()

items = {'id': ids, 'title': titles, 'cluster': clusters, 'description': ds, 'price': prices}
frame = pd.DataFrame(items, index = [clusters] , columns = ['id', 'title', 'cluster', 'description', 'price'])


#MDS here
dist = 1 - cosine_similarity(ds_tfidf)
MDS()
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist)
xs, ys = pos[:, 0], pos[:, 1]


#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#16b22f', 6: '#65d21a'}
av_prices = frame['price'].groupby(frame['cluster']).mean()


df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles))
groups = df.groupby('label')




#Setup plots
fig, ax = plt.subplots(figsize=(17, 9)) # set size
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling


for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, alpha=0.4,
            label='$%s' % round(av_prices[name], 2), color=cluster_colors[name], 
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')

ax.legend(numpoints=1)  #show legend with only 1 point

#add label in x,y position with the label as the film title
i = 0
while i < len(df):
    ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)
    i += 200

plt.show()



code.interact(local=locals())

