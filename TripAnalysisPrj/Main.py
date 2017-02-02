import TripsApiService as envService
import yaml


def read_file(file_name):
    with open(file_name, 'r') as myfile:
        data = myfile.read().replace('\n', '')
        trip = yaml.load(data)
        print(trip)

trips = envService.CarService.get_car_trips(2, 10)  # Range found: 1 - 70 for limit = 100

print("{0}:".format(len(trips)))

for trip in trips.values():
    dumped_trip = yaml.dump(trip)
    file = open('./data/{0}.trip'.format(trip.get_id()), 'w+')
    file.write(dumped_trip)
    file.close()
    print(trip)

# read_file('./data/588e364de4b04a0d732d7356.dat')
