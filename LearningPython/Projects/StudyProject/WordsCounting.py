__author__ = 'askofen'

from sklearn.feature_extraction.text import CountVectorizer
import os
import scipy as sp
import sys
import nltk.stem
from sklearn.feature_extraction.text import TfidfVectorizer

vect = CountVectorizer(min_df=1)
data = ["How to learn machine learning", "Using python for machine learning"]
x = vect.fit_transform(data)
print(vect.get_feature_names())
print(x.toarray().transpose())

dir = "../../Data/03/data/toy"

posts = [open(os.path.join(dir, f)).read() for f in os.listdir(dir)]
vectorizer = CountVectorizer(min_df = 1)
x_train = vectorizer.fit_transform(posts)
num_samples, num_features = x_train.shape

print(num_samples)
print(num_features)
print(vectorizer.get_feature_names())

new_post = "imaging databases"
new_post_vec = vectorizer.transform([new_post])

print(new_post_vec)
print(new_post_vec.toarray())

def dist_raw(v1, v2):
    delta = v1 - v2
    return sp.linalg.norm(delta.toarray())

def dist_norm(v1, v2):
    v1_n = v1/sp.linalg.norm(v1.toarray())
    v2_n = v2/sp.linalg.norm(v2.toarray())
    delta = v1_n - v2_n
    return sp.linalg.norm(delta.toarray())

best_doc = None
best_dist = sys.maxint
best_i = None

for i in range(0, num_samples):
    post = posts[i]

    if (post == new_post):
        continue

    post_vec = x_train.getrow(i)
    d = dist_norm(post_vec, new_post_vec)

    print(i, d, post)

    if d<best_dist:
        best_dist = d
        best_i = i


print
print(best_i)
print(best_dist)
print(posts[best_i])

vect_stop = CountVectorizer(min_df=1, stop_words='english')
print(vect_stop.get_stop_words())

eng_stremmer = nltk.stem.SnowballStemmer('english')

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda  doc: (eng_stremmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedCountVectorizer(min_df=1, stop_words='english')
x_train = vectorizer.fit_transform(posts)

print(vectorizer.get_feature_names())
print(x_train.toarray())

class StemmedTfidVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidVectorizer, self).build_analyzer()
        return lambda  doc: (eng_stremmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedTfidVectorizer(min_df=1, stop_words='english')
x_train = vectorizer.fit_transform(posts)

print(vectorizer.get_feature_names())
print(x_train.toarray())
print(posts)