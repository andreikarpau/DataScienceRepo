import json


class FileHelper:
    @staticmethod
    def read_json_file(name):
        all_properties = []

        with open(name, "r") as json_file:
            for line in json_file:
                item = json.loads(line)
                all_properties.append(item)

        return all_properties