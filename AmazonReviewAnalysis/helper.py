import json


class FileHelper:
    @staticmethod
    def read_data_file(name):
        texts = []
        summaries = []
        overall = []

        with open(name, "r") as json_file:
            for line in json_file:
                str = json.loads(line)
                texts.append(str["reviewText"])
                summaries.append(str["summary"])
                overall.append(str["overall"])

        return texts, summaries, overall
