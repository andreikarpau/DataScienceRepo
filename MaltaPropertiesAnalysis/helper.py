import json

import numpy as np


class FileHelper:
    @staticmethod
    def read_json_file(name):
        all_properties = []

        with open(name, "r") as json_file:
            for line in json_file:
                item = json.loads(line)
                all_properties.append(item)

        return all_properties

    @staticmethod
    def get_geocoded_data():
        data = FileHelper.read_json_file("data/geocoded_properties_info.json")

        ids = []
        bedrooms = []
        prices = []
        latitudes = []
        longitudes = []
        bedroom_prices = []

        for d in data:
            lat = float(d["latitude"])
            lon = float(d["longitude"])
            if lat < 35.7 or 36.1 < lat or lon < 14.1 or 14.6 < lon:
                continue

            ids.append(d["id"])
            bedrooms.append(int(d["bedrooms"]))
            prices.append(int(d["price"]))
            latitudes.append(lat)
            longitudes.append(lon)
            bedroom_prices.append(int(d["price"]) / int(d["bedrooms"]))

        return np.asarray(ids), np.asarray(bedrooms), np.asarray(prices), np.asarray(latitudes), np.asarray(longitudes), np.asarray(bedroom_prices)