import TripsApiService as envService

trips = envService.CarService.get_car_trips(1, 10)  # Range found: 1 - 70 for limit = 100

print("{0}:".format(len(trips)))

for trip in trips.values():
    print(trip)
