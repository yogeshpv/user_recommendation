__author__ = 'veettily'

import nltk
import string
import os
import re
import unidecode
import operator
import pprint
import math
import json
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
pp = pprint.PrettyPrinter(indent=2)

file = '/home/ubuntu/tweets/processed_output_SF.out'
d = defaultdict(list)

with open(file) as f:
    for row in f:
        tweet_info = json.loads(row)
        d[tweet_info['user_screen_name']].append(tweet_info['text'])

def lemmatize_tokens(tokens, lemmatizer):
    lemmatized = []
    for item in tokens:
        lemmatized.append(lemmatizer.lemmatize(item))

    return lemmatized

def tokenize(text):
    tknzr = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
    lemmatizer = WordNetLemmatizer()
    tokens = tknzr.tokenize(text)
    lemmatized = lemmatize_tokens(tokens, lemmatizer)
    return lemmatized

def get_word_corpus(twitter_user):
    tweets = []
    for tweet in d[twitter_user]:
        tweets.append(tweet)
    return tweets

model_dict = defaultdict()
d_new = defaultdict()

for twitter_user in d.keys():
    num_topics = int(np.sqrt(len(d[twitter_user])))
    try:
        model = NMF(n_components=num_topics, init='random', random_state=0)
        tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
        tfidf_vector = tfidf.fit_transform(d[twitter_user])
        #         model.fit(tfidf_vector)
        W = model.fit_transform(tfidf_vector)
    except:
        continue

    model_dict[twitter_user] = defaultdict(list)
    model_dict[twitter_user]['model'] = model
    model_dict[twitter_user]['tfidf'] = tfidf
    model_dict[twitter_user]['tfidf_vector'] = tfidf_vector
    model_dict[twitter_user]['W'] = W

    d_new[twitter_user] = d[twitter_user]

# d['brainneeblove']
# https://ec2-54-87-219-125.compute-1.amazonaws.com:8888/tree#

id2word = defaultdict()
for twitter_user in d_new.keys():
    id2word[twitter_user] = defaultdict()
    for keyword, index in model_dict[twitter_user]['tfidf'].vocabulary_.iteritems():
        id2word[twitter_user][index] = keyword

with open('topic_out.out', 'a') as out:
    for twitter_user in d_new.keys():
        out.writelines('------' + twitter_user + '------\n')
        model = model_dict[twitter_user]['model']
        out.writelines(str(id2word[twitter_user].values()[:15])+ '\n')

from gensim.models import Word2Vec
def get_word_vector_model(model_path = "glove.6B.50d.txt"):
    print("Loading model {}. May take several minutes depending on size...".format(model_path))
    return Word2Vec.load_word2vec_format(model_path)

results = spelling_model.most_similar(positive=pos_vector_search_list + [spellings_mean], negative=neg_vector_search_list)