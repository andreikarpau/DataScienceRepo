__author__ = 'askofen'
from gensim import corpora, models, similarities
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

corpus = corpora.BleiCorpus('../../Data/04/data/ap.dat', '../../Data/04/data/vocab.txt')

# alpha = 1 -> more topics per document
model = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=corpus.id2word)

# length of vocabulary dictionary
print(len(model.id2word))

topics = [model[topic] for topic in corpus]
topicsProDocCount = [len(t) for t in topics]

plt.hist(topicsProDocCount, bins=15)
plt.title("Topics pro document histogram")

dense = np.zeros((len(topics), 100), float)

# make matrix with weight of each topic for each document
for ti, t in enumerate(topics):
    for tj, v in t:
        dense[ti, tj] = v

#distance between all the rows in the matrix
pairwise = distance.squareform(distance.pdist(dense))

largest = pairwise.max()

#Trick: make all diagonal values to be the largers (get rid of 0 values)
for ti in range(len(topic)):
    pairwise[ti,ti] = largest + 1

#returns the closest document id to document with id = doc_id
def closest_to(doc_id):
    return pairwise[doc_id].argmin()