import TripsApiService as envService
import yaml
import os
from CarTrip import TripHelper


def read_trip_file(file_name):
    with open(file_name, 'r') as trip_file:
        data = trip_file.read() #.replace('\n', '')
        loaded_trip = yaml.load(data)
        return loaded_trip

def download_and_save():
    # Ranges downloaded: 1,10;2,10;10,10;11,10;20,10;25,10;
    trips = envService.CarService.get_car_trips(25, 10)  # Range found: 1 - 70 for limit = 100

    print("{0}:".format(len(trips)))

    for trip in trips.values():
        dumped_trip = yaml.dump(trip)
        file = open('./data/{0}.trip'.format(trip.get_id()), 'w+')
        file.write(dumped_trip)
        file.close()
        print(trip)

    # read_file('./data/588e364de4b04a0d732d7356.dat')

def read_all_trip_files():
    entries = os.scandir('./data/')
    trips = []

    for f in entries:
        if not f.is_file():
            continue

        trip = read_trip_file(f.path)
        trips.append(trip)

    return trips

trips = read_all_trip_files()
measures, tags = TripHelper.get_all_measures_tags_names(trips)

for trip in trips:
    keys, lines = trip.save_to_array(measures, tags)


print(trips)
