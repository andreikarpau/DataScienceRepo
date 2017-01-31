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
    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude


class Road:
    def __init__(self, display_name, osm_id, tags):
        self.__display_name = display_name
        self.__osm_id = osm_id
        self.__tags = tags

    def check_place(self, place_name):
        dn = self.__display_name.lower()
        return place_name.strip().lower() in dn
