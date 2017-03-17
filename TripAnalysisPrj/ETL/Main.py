import TripsApiService as envService
import yaml
import os
import csv
from CarTrip import TripHelper
from os import path
import collections


def read_trip_file(file_name):
    with open(file_name, 'r') as trip_file:
        data = trip_file.read()  # .replace('\n', '')
        loaded_trip = yaml.load(data)
        return loaded_trip


def download_and_save(values=[[1, 10]]):
    for value in values:
        # Ranges downloaded: 1,10;2,10;10,10;11,10;20,10;25,10;30,10;40,10;50,10;130,10;160, 10;170,10;180,30;230,10;
        #250,30;280,20
        trips = envService.CarService.get_car_trips(value[0], value[1])  # Range found: 1 - 70 for limit = 100

        print("{0}:".format(len(trips)))

        for trip in trips.values():
            dumped_trip = yaml.dump(trip)
            file = open('./data/{0}.trip'.format(trip.get_id()), 'w+')
            file.write(dumped_trip)
            file.close()
            print(trip)


def read_all_trip_files():
    entries = os.scandir('./data/input/')
    trips = []

    for f in entries:
        if not f.is_file():
            continue

        trip = read_trip_file(f.path)
        trips.append(trip)

    return trips


def read_and_save_trips_to_csvs():
    trips = read_all_trip_files()
    measures, tags = TripHelper.get_all_measures_tags_names(trips)

    measures = collections.OrderedDict(sorted(measures.items(), reverse=True))
    tags = collections.OrderedDict(sorted(tags.items()))

    TripHelper.remove_items_from_dict(tags, ["source:ref", "created_by", "oneway:bicycle", "maxspeed:source", "note",
                                             "source", "access", "layer", "hgv", "source:maxspeed:backward",
                                             "source:maxspeed:forward",
                                             "cycleway: segregated", "segregated", "description", "service",
                                             "motor_vehicle", "abandoned:highway", "bridge_ref", "change:lanes",
                                             "oneway: psv", "tracktype", "construction", "source:maxspeed:backward",
                                             "source:maxspeed:forward", "cutting", "source:maxspeed", "hazmat",
                                             "maxweight", "strassen-nrw:abs", "cycleway:left", "cycleway:right",
                                             "name:etymology:wikidata", "name:etymology:wikipedia",
                                             "placement", "is_in", "note:name", "reg_name", "noexit", "place_numbers",
                                             "maxheight", "motorcar", "motorcycle", "motorroad", "name", "ref",
                                             "osmarender:nameDirection", "source:lit", "minspeed", "oneway:psv",
                                             "cycleway:segregated", "smoothness", "destination", "destination:lanes",
                                             "toll:N3", "postal_code", "zone:traffic", "lanes:backward",
                                             "lanes:forward", "turn:lanes:forward", "maxspeed:backward",
                                             "maxspeed:forward", "strassen - nrw: abs", "turn", "voltage", "incline",
                                             "int_ref", "embankment", "maxspeed:variable", "vehicle", "agricultural",
                                             "emergency", "goods", "horse", "hov", "overtaking",
                                             "turn:lanes:backward", "turn:lanes", "tunnel", "sidewalk", "psv",
                                             "junction", "bridge", "foot", "opening_date", "railway", "start_date",
                                             "cycleway: left", "cycleway: right", "electrified",
                                             "abandoned: highway", "abutters", "alt_ref", "bicycle", "bridge_ref"
                                                                                                     "change: lanes"])

    measures_units_list = {}

    for trip in trips:
        print("Processing {0}".format(trip))

        keys, lines, trip_id, car_name_id = trip.save_to_array(measures, tags, measures_units_list)
        if trip_id is None:
            continue

        file_name = './csv/{0}.csv'.format(car_name_id)
        add_header = not path.isfile(file_name)

        with open(file_name, 'a', newline='') as f:
            writer = csv.writer(f)

            if add_header:
                writer.writerow(keys)

            writer.writerows(lines)

    with open("./csv/MeasuresUnits.txt", "w") as text_file:
        for measures_units in measures_units_list:
            units_string = measures_units + ": "

            for units in measures_units_list[measures_units]:
                units_string += units + "; "

            text_file.write(units_string + "\n")


def reread_file():
    trips = read_all_trip_files()
    for trip in trips:
        for measure in trip.get_measurements().values():
            road = measure.get_road();
            envService.CarService.add_road_to_cache(road, measure.get_latitude(), measure.get_longitude())

    download_and_save([[1, 10], [2, 10], [10, 10], [11, 10], [20, 10], [25, 10]])


#download_and_save([[280,20]])
read_and_save_trips_to_csvs()
