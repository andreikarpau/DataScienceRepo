import json
import matplotlib.pyplot as plt
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
                if max_num is not None and max_num <= iteration:
                    break

                str = json.loads(line)

                rate = str["overall"]
                # if rate == 3:
                #     continue
                #
                iteration = iteration + 1

                texts.append(str["reviewText"])
                summaries.append(str["summary"])
                overall.append(rate)

        return texts, summaries, overall

    @staticmethod
    def read_word2vec(file_name="word2vec/glove.6B.50d.txt"):
        with open(file_name, "rb") as lines:
            w2v = {line.split()[0]: np.array(map(float, line.split()[1:]))
                   for line in lines}
            return w2v

    @staticmethod
    def get_sample_data_rates():
        return FileHelper.read_data_file("data/balanced_sample.json")
