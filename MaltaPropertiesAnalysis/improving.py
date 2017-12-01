from helper import FileHelper
import json

data = FileHelper.read_json_file("data/geocoded_properties_info.json")

for d in data:
    if d["place"] == "Gozo - Xaghra":
        d["latitude"] = 36.051303
        d["longitude"] = 14.267890

    if d["place"] == "Gozo - Qala":
        d["latitude"] = 36.035591
        d["longitude"] = 14.314627

    if d["place"] == "Dingli":
        d["latitude"] = 35.860394
        d["longitude"] = 14.382788

    if d["place"] == "Gozo - Fontana":
        d["latitude"] = 36.037855
        d["longitude"] = 14.235865

    if d["place"] == "Pieta":
        d["latitude"] = 35.893096
        d["longitude"] = 14.493920

    if d["place"] == "Gozo - Ghasri":
        d["latitude"] = 36.068941
        d["longitude"] = 14.222510

    if d["place"] == "Gozo - Kercem":
        d["latitude"] = 36.041321
        d["longitude"] = 14.223779


with open('data/geocoded_properties_info.json', 'w') as file:
    for p in data:
        json_str = json.dumps(p).encode('utf8').decode('utf8')
        file.write(json_str)
        file.write('\n')