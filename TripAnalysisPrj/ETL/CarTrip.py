import dateutil.parser
from astral import Astral
import operator


class Trip:
    def __init__(self, api_id, length, car, measurements):
        self.__id = api_id
        self.__length = length
        self.__car = car
        self.__measurements = measurements

    def get_id(self):
        return self.__id

    def get_car(self):
        return self.__car

    def get_measurements(self):
        return self.__measurements

    def __str__(self):
        return "Trip {0}, Length {1}; {2}".format(self.__id, self.__length, self.__car)

    def get_simple_params(self):
        return self.__id, self.__length

    def save_to_array(self, measures_keys, tags_keys, units_list, value_to_verify="CO2_value"):
        trip_array = [];

        all_keys = ["trip_id", "trip_length", "car_id", "car_construction_year", "car_engine_displacement",
                    "car_fuel_type", "car_manufacturer", "car_model", "measure_index", "latitude", "longitude",
                    "time", "time_type", "time_light_type_num", "road_name", "osmap_id"];

        all_keys.extend(measures_keys)
        all_keys.extend(tags_keys)

        for measurement in self.get_measurements().values():
            line = [];
            line.extend(self.get_simple_params())
            line.extend(self.get_car().get_all_params())
            line.extend(measurement.get_simple_params())
            line.extend(measurement.get_road().get_simple_params())

            measures = measurement.get_measures()
            road_tags = measurement.get_road().get_tags()

            if not (value_to_verify in measures):
                return None, None, None, None

            for measures_key in measures_keys:
                if measures_key in measures:
                    unit_name = measures[measures_key]
                    line.append(unit_name)

                    if "_unit" in measures_key:
                        if not (measures_key in units_list):
                            units_list[measures_key] = {}

                        units_list[measures_key][unit_name] = True
                else:
                    line.append(None)

            for tag_key in tags_keys:
                if tag_key in road_tags:
                    line.append(road_tags[tag_key])
                else:
                    line.append(None)

            trip_array.append(line)

        return all_keys, trip_array, self.get_id(), self.get_car().get_car_unique_name()


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

    def get_car_unique_name(self):
        return "{0}_{1}_{2}".format(self.__manufacturer, self.__model, self.__api_id)

    def get_id(self):
        return self.__api_id

    def get_all_params(self):
        return self.__api_id, self.__construction_year, self.__engine_displacement, self.__fuel_type, self.__manufacturer, self.__model


class Measurement:
    def __init__(self, index, latitude, longitude, road, time, odb2_measures):
        self.__index = index
        self.__latitude = latitude
        self.__longitude = longitude
        self.__road = road
        self.__time = time
        self.__measures = {}

        for key, value in odb2_measures.items():
            self.__measures[key + "_value"] = value["value"]
            self.__measures[key + "_unit"] = value["unit"]

    def get_simple_params(self):
        datetime = dateutil.parser.parse(self.__time)
        time_type, time_light_type_num = TripHelper.day_time_definition(datetime)

        return self.__index, self.__latitude, self.__longitude, self.__time, time_type, time_light_type_num

    def get_measures(self):
        return self.__measures

    def get_longitude(self):
        return self.__longitude

    def get_latitude(self):
        return self.__latitude

    def get_road(self):
        return self.__road;


class Road:
    def __init__(self, display_name, osm_id, tags):
        self.__display_name = display_name
        self.__osm_id = osm_id
        self.__tags = tags

    def get_simple_params(self):
        return self.__display_name, self.__osm_id

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
    def day_time_definition(datetime):
        astral_obj = Astral()
        astral_obj.solar_depression = 'civil'
        city = astral_obj["Berlin"]
        sun_info = city.sun(date=datetime, local=True)

        if datetime < sun_info["dawn"]:
            return "night", 0

        if datetime < sun_info["sunrise"]:
            return "dawn", 1

        if datetime < sun_info["sunset"]:
            return "daylight", 2

        if datetime < sun_info["dusk"]:
            return "dusk", 1

        return "night", 0

    @staticmethod
    def remove_items_from_dict(the_dict, entries):
        for key in entries:
            if key in the_dict:
                del the_dict[key]

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
