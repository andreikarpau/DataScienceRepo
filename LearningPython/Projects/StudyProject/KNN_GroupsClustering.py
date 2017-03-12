__author__ = 'askofen'
import sklearn.datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk.stem
import scipy as sp

ML_DIR = "../../Data/03/data"
data = sklearn.datasets.load_mlcomp("20news-18828", mlcomp_root=ML_DIR)

print(len(data.filenames))
print(data.target_names)

groups = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x', 'sci.space']

train_data = sklearn.datasets.load_mlcomp("20news-18828", "train", mlcomp_root=ML_DIR, categories=groups)
test_data = sklearn.datasets.load_mlcomp("20news-18828", "test", mlcomp_root=ML_DIR, categories=groups)

print(len(train_data.filenames))
print(len(test_data.filenames))

eng_stremmer = nltk.stem.SnowballStemmer('english')

class StemmedTfidVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidVectorizer, self).build_analyzer()
        return lambda  doc: (eng_stremmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedTfidVectorizer(min_df=10, max_df=0.5, stop_words='english', decode_error='ignore')
vectorized = vectorizer.fit_transform(train_data.data)

print(vectorized.shape)

num_clusters = 50
km = KMeans(n_clusters = num_clusters, init='random', n_init = 1, verbose = 1)
km.fit(vectorized)

print(km.labels_)
print(km.labels_.shape)

new_post = "Disk drive problems. Hi, I have a problem with my hard disk. After 1 year it is working only sporadically now. I tried to format it, but now it doesn't boot any more. Any ideas? Thanks."
new_post_vec = vectorizer.transform([new_post])

print(new_post_vec.nonzero()[1])

new_post_label = km.predict(new_post_vec)
new_post_label = new_post_label[0]
print(new_post_label)

similiar_indices = (km.labels_ == new_post_label).nonzero()[0]
print(similiar_indices)

#Find most similar posts
similar = []
for i in similiar_indices:
    dist = sp.linalg.norm((new_post_vec - vectorized[i]).toarray())
    similar.append((dist, train_data.data[i]))


similar = sorted(similar)
print(len(similar))
print(similar[0])

post_group = zip(data.data, data.target)

#low power word
print(vectorizer._tfidf.idf_[vectorizer.vocabulary_['thank']])

#high power word
print(vectorizer._tfidf.idf_[vectorizer.vocabulary_['bh']])