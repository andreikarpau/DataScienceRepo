import CarTrip
import requests


class CarService:
    def __init__(self):
        pass

    @staticmethod
    def get_car_trips(page=1, limit_trips=100):
        response = requests.get('https://envirocar.org/api/stable/tracks?limit={0}&page={1}'.format(limit_trips, page))
        tracks_data = response.json()
        tracks = tracks_data['tracks']
        trips = {}

        for value in tracks:
            info = value['sensor']

            if info['type'] != 'car':
                continue

            properties = info['properties']
            car = CarTrip.Car(properties['id'], properties['constructionYear'], properties['engineDisplacement'],
                              properties['fuelType'], properties['manufacturer'], properties['model'])

            trip_id = value['id']
            measurements = CarService.get_car_measurements(trip_id)
            trip = CarTrip.Trip(trip_id, value['length'], car, measurements)

            trips[trip.get_id()] = trip

        return trips

    @staticmethod
    def get_car_measurements(tripId):
        measurements = {}
        index = 0

        response = requests.get('https://envirocar.org/api/stable/tracks/{0}/measurements'.format(tripId))
        features = response.json()['features']

        for value in features:
            latitude = value['geometry']['coordinates'][1]
            longitude = value['geometry']['coordinates'][0]

            road = CarService.get_road_info(latitude, longitude)

            measurements[index] = CarTrip.Measurement(value['geometry']['coordinates'][1],
                                                      value['geometry']['coordinates'][0])
            index += 1

        return measurements


    @staticmethod
    def get_road_info(latitude, longitude):
        response = requests.get('http://nominatim.openstreetmap.org/reverse.php?format=json&lat={0}&lon={1}&zoom=16'.format(latitude, longitude))
        road = response.json()

        road_name = road['display_name']
        osm_id = road['osm_id']

        # response_osm = requests.get('http://www.openstreetmap.org/api/0.6/way/{0}'.format(osm_id))
        # road_info = response_osm.xml

        return road_name
