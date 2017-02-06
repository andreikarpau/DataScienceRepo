class Trip:
    def __init__(self, api_id, length, car, measurements):
        self.__id = api_id
        self.__length = length
        self.__car = car
        self.__measurements = measurements

    def get_id(self):
        return self.__id

    def get_measurements(self):
        return self.__measurements

    def __str__(self):
        return "Trip {0}, Length {1}; {2}".format(self.__id, self.__length, self.__car)

    def get_simple_params(self):
        return self.__id, self.__length

    def save_to_array(self, measures_keys, tags_keys):
        trip_array = [];
        all_keys = ["trip_id", "trip_length", "car_id", "car_construction_year", "car_engine_displacement", "car_fuel_type",
                    "car_manufacturer", "car_model"];

        for measurement in self.get_measurements().values():
            line = [];
            line.extend(self.get_simple_params())
            line.extend(self.__car.get_all_params())

            trip_array.append(line)

        return all_keys, trip_array


class Car:
    def __init__(self, api_id, construction_year, engine_displacement, fuel_type, manufacturer, model):
        self.__api_id = api_id
        self.__construction_year = construction_year
        self.__engine_displacement = engine_displacement
        self.__fuel_type = fuel_type
        self.__manufacturer = manufacturer
        self.__model = model

    def __str__(self):
        return "Car {0}: {1} {2} {3} {4} {5}".format(self.__api_id, self.__manufacturer, self.__model,
                                                     self.__engine_displacement, self.__fuel_type,
                                                     self.__construction_year)

    def get_id(self):
        return self.__api_id

    def get_all_params(self):
        return self.__api_id, self.__construction_year, self.__engine_displacement, self.__fuel_type, self.__manufacturer, self.__model

class Measurement:
    def __init__(self, index, latitude, longitude, road, odb2_measures):
        self.__index = index
        self.__latitude = latitude
        self.__longitude = longitude
        self.__road = road
        self.__measures = {}

        for key, value in odb2_measures.items():
            self.__measures[key + "_value"] = value["value"]
            self.__measures[key + "_unit"] = value["unit"]

    def get_measures(self):
        return self.__measures

    def get_road(self):
        return self.__road;


class Road:
    def __init__(self, display_name, osm_id, tags):
        self.__display_name = display_name
        self.__osm_id = osm_id
        self.__tags = tags

    def get_tags(self):
        return self.__tags

    def check_place(self, place_names):
        dn = self.__display_name.lower()
        for place in place_names:
            if place.strip().lower() in dn:
                return True

        return False


class TripHelper:
    @staticmethod
    def get_all_measures_tags_names(trips):
        measures = {}
        tags = {}

        for trip in trips:
            for measurement in trip.get_measurements().values():
                for measure_key in measurement.get_measures().keys():
                    measures[measure_key] = "";

                for tag_key in measurement.get_road().get_tags().keys():
                    tags[tag_key] = "";

        return measures, tags
