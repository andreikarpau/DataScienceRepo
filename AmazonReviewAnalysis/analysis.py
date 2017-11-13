import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from PreprocessingEngine import PreprocessingEngine
from helper import FileHelper


texts, summaries, overalls = FileHelper.get_sample_data_rates()

texts = np.asarray(texts)
summaries = np.asarray(summaries)
overalls = np.asarray(overalls)


preprocessingEngine = PreprocessingEngine()
vectorizer = CountVectorizer(tokenizer=preprocessingEngine.tweet_tokenize_stemming)

texts_matrix = vectorizer.fit_transform(texts)

freqs = [(word, texts_matrix.getcol(idx).sum()) for word, idx in vectorizer.vocabulary_.items()]
counts_sorted = sorted (freqs, key = lambda x: -x[1])

#######################################################
print(counts_sorted)

counts_dict = {}
for item in counts_sorted:
    counts_dict[item[0]] = item[1]

FileHelper.show_word_cloud(counts_dict)