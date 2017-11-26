import json
import re
#import geocoder
from mapbox import Geocoder
from helper import FileHelper

properties = FileHelper.read_json_file("data/malta_villa_properties.json")
properties_bungalow = FileHelper.read_json_file("data/malta_bungalow_properties.json")

properties.extend(properties_bungalow)

ids = {}
properties_adjusted = []

mapbox_token = "bla"
geocoder = Geocoder(access_token=mapbox_token)

count = 0
for p in properties:
    # count = count + 1
    # if 10 < count :
    #     break

    try:
        if p['id'] in ids:
            continue

        ids[p['id']] = True

        bedrooms = None
        house_type = None
        place = re.search('For Sale in (.+?)$', p['title']).group(1)

        bedrooms_group = re.search('.*(\d+?) +Bedroom.*', p['title'])
        if bedrooms_group:
            bedrooms = bedrooms_group.group(1)
            bedrooms = (bedrooms if 0 < int(bedrooms) else None)
            house_type = re.search('Bedroom *(.+?) +For Sale.*', p['title']).group(1)
        else:
            house_type = re.search(' *(.+?) +For Sale.*', p['title']).group(1)

        price_str = ""
        for s in re.findall(r'\d+', p['price']):
            price_str += s

        price = int(price_str) if price_str else None

        size = None
        if 'Size' in p['details']:
            size = int(re.search('\d+', p['details']['Size']).group(0))


        response = geocoder.forward('{0}, Malta'.format(place), lat=35.937496, lon=14.375416)
        if response.status_code != 200:
            continue

        coordinates = response.geojson()['features'][0]['geometry']['coordinates']
        print("{0} {1} {2} {3} {4} {5}".format(bedrooms, house_type, place, price, size, coordinates))

        if bedrooms and price:
            properties_adjusted.append({'id': p['id'], 'bedrooms': bedrooms, 'house_type': house_type,
                                        'place': place, 'price': price, 'size': size, 'latitude': coordinates[1],
                                        'longitude': coordinates[0],
                                        'features': p['features'],
                                        'description': p['description']})

    except ValueError:
        print("ValueError")
    except:
        print("Error")


print(properties_adjusted)
print(len(properties_adjusted))

with open('data/geocoded_properties_info.json', 'w') as file:
    for p in properties_adjusted:
        json_str = json.dumps(p).encode('utf8').decode('utf8')
        file.write(json_str)
        file.write('\n')

