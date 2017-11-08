import nltk
from sklearn.feature_extraction.text import CountVectorizer
from helper import FileHelper

texts, summaries, overalls = FileHelper.get_sample_data_rates()

tokens = nltk.word_tokenize(texts)
print(tokens)

# vectorizer = CountVectorizer()
#
# texts_matrix = vectorizer.fit_transform(texts)
#
# freqs = [(word, texts_matrix.getcol(idx).sum()) for word, idx in vectorizer.vocabulary_.items()]
# freqs_sorted = sorted (freqs, key = lambda x: -x[1])
# print(freqs_sorted)