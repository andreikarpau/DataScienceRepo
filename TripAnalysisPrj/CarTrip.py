class Trip:
    def __init__(self, api_id, length, car, measurements):
        self.__id = api_id
        self.__length = length
        self.__car = car
        self.__measurements = measurements

    def get_id(self):
        return self.__id

    def __str__(self):
        return "Trip {0}, Length {1}; {2}".format(self.__id, self.__length, self.__car)

    # def get_as_string(self):
    #     final_str = ""
    #     for measure in self.__measurements:
    #         measure.

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

    def get_road(self):
        return self.__road;

class Road:
    def __init__(self, display_name, osm_id, tags):
        self.__display_name = display_name
        self.__osm_id = osm_id
        self.__tags = tags

    def check_place(self, place_names):
        dn = self.__display_name.lower()
        for place in place_names:
            if place.strip().lower() in dn:
                return True

        return False
