import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np


class FileHelper:
    @staticmethod
    def read_data_file(name, max_num=None):
        texts = []
        summaries = []
        overall = []

        iteration = 0
        with open(name, "r") as json_file:
            for line in json_file:
                iteration = iteration + 1
                if max_num is not None and max_num <= iteration:
                    break

                str = json.loads(line)

                rate = str["overall"]
                if rate == 3:
                    continue

                texts.append(str["reviewText"])
                summaries.append(str["summary"])
                overall.append(rate)

        return texts, summaries, overall

    @staticmethod
    def generate_word_cloud(vectorizer, text):
        d = {}

        corpus = vectorizer.fit_transform(text)
        i = 0
        for name in vectorizer.get_feature_names():
            d[name] = corpus[i]
            i += 1

        wordcloud = WordCloud()
        wordcloud.generate_from_frequencies(frequencies=d)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    @staticmethod
    def read_word2vec(file_name="word2vec/glove.6B.50d.txt"):
        with open(file_name, "rb") as lines:
            w2v = {line.split()[0]: np.array(map(float, line.split()[1:]))
                   for line in lines}
            return w2v
