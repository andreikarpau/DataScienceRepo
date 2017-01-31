import CarTrip
import requests
import xml.etree.ElementTree as elementTree
import time


class CarService:
    def __init__(self):
        pass

    __roads_id_cache = {}
    __roads_coordinates_cache = {}

    @staticmethod
    def get_car_trips(page=1, limit_trips=100):
        response = requests.get('https://envirocar.org/api/stable/tracks?limit={0}&page={1}'.format(limit_trips, page))
        tracks_data = response.json()
        tracks = tracks_data['tracks']
        trips = {}
        check_index = 0;

        for value in tracks:
            try:
                info = value['sensor']

                if info['type'] != 'car':
                    continue

                properties = info['properties']
                car = CarTrip.Car(properties['id'], properties['constructionYear'], properties['engineDisplacement'],
                                  properties['fuelType'], properties['manufacturer'], properties['model'])

                trip_id = value['id']

                measurements = CarService.get_car_measurements(trip_id, "Mönchengladbach") #Mönchengladbach
                if measurements is None:
                    continue

                tripLength = None if 'length' not in value else value['length']
                trip = CarTrip.Trip(trip_id, tripLength, car, measurements)

                trips[trip.get_id()] = trip
            except Exception as e:
                print('Exception in tracks on index = <{0}>. Exception: {1}'.format(check_index, e))

            check_index += 1

        return trips

    @staticmethod
    def get_car_measurements(trip_id, place):
        measurements = {}
        index = 0

        response = requests.get('https://envirocar.org/api/stable/tracks/{0}/measurements'.format(trip_id))
        features = response.json()['features']

        place_checked = False

        for value in features:
            latitude = value['geometry']['coordinates'][1]
            longitude = value['geometry']['coordinates'][0]

            road = CarService.get_road_info(latitude, longitude)

            if not place_checked:
                place_checked = True
                if not road.check_place(place):
                    return None

            measurements[index] = CarTrip.Measurement(value['geometry']['coordinates'][1],
                                                      value['geometry']['coordinates'][0])
            index += 1

        return measurements

    @staticmethod
    def get_road_info(latitude, longitude):
        lat_lot_hash = latitude + longitude;

        if lat_lot_hash in CarService.__roads_coordinates_cache:
            return CarService.__roads_coordinates_cache[lat_lot_hash]

        time.sleep(1)

        response = requests.get(
            'http://nominatim.openstreetmap.org/reverse.php?format=json&lat={0}&lon={1}&zoom=16'.format(latitude,
                                                                                                        longitude))
        road = response.json()

        osm_id = road['osm_id']

        if osm_id in CarService.__roads_id_cache:
            return CarService.__roads_id_cache[osm_id]

        road_name = road['display_name']

        response_osm = requests.get('http://www.openstreetmap.org/api/0.6/way/{0}'.format(osm_id))
        way = elementTree.fromstring(response_osm.text).find("way")
        tags = {}

        if way is not None:
            for tag in way.iter("tag"):
                key = tag.attrib["k"]
                value = tag.attrib["v"]
                tags[key] = value

        road = CarTrip.Road(road_name, osm_id, tags);
        CarService.__roads_coordinates_cache[lat_lot_hash] = road
        CarService.__roads_id_cache[osm_id] = road
        return road
