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
        self.__apiId = api_id
        self.__constructionYear = construction_year
        self.__engineDisplacement = engine_displacement
        self.__fuelType = fuel_type
        self.__manufacturer = manufacturer
        self.__model = model

    def __str__(self):
        return "Car {0}: {1} {2} {3} {4} {5}".format(self.__apiId, self.__manufacturer, self.__model,
                                                     self.__engineDisplacement, self.__fuelType,
                                                     self.__constructionYear)

    def get_id(self):
        return self.__apiId


class Measurement:
    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude
