import numpy as np
import random
import json

class Taxi_Location:
    num = 0
    max_lat = 40.89985962
    min_lat = 40.52729818
    max_lon = -73.70907059
    min_lon = -74.22954655
    mean_deglat_per_10s = 4.99062E-04
    mean_deglon_per_10s = 7.058267E-04

    def __init__(self):
        self.id = Taxi_Location.num
        Taxi_Location.num += 1
        self.latitude = (Taxi_Location.min_lat + (Taxi_Location.max_lat-Taxi_Location.min_lat)/1000*random.randrange(1000))
        self.longitude = (Taxi_Location.min_lon + (Taxi_Location.max_lon-Taxi_Location.min_lon)/1000*random.randrange(1000))

        # self.latitude = np.random.normal(((Taxi_Location.min_lat+Taxi_Location.max_lat)/2),((Taxi_Location.max_lat-Taxi_Location.min_lat)/3))
        # self.longitude = np.random.normal(((Taxi_Location.min_lon+Taxi_Location.max_lon)/2),((Taxi_Location.max_lon-Taxi_Location.min_lon)/3))

    def randomise(self):
        if random.randrange(2):
            self.latitude += np.random.normal(Taxi_Location.mean_deglat_per_10s,Taxi_Location.mean_deglat_per_10s/2)
        else:
            self.latitude -= np.random.normal(Taxi_Location.mean_deglat_per_10s,Taxi_Location.mean_deglat_per_10s/2)
        if self.latitude < Taxi_Location.min_lat:
            self.latitude = Taxi_Location.min_lat
        elif self.latitude > Taxi_Location.max_lat:
            self.latitude = Taxi_Location.max_lat

        if random.randrange(2):
            self.longitude += np.random.normal(Taxi_Location.mean_deglon_per_10s,Taxi_Location.mean_deglon_per_10s/2)
        else:
            self.longitude -= np.random.normal(Taxi_Location.mean_deglon_per_10s,Taxi_Location.mean_deglon_per_10s/2)
        if self.longitude < Taxi_Location.min_lon:
            self.longitude = Taxi_Location.min_lon
        elif self.longitude > Taxi_Location.max_lon:
            self.longitude = Taxi_Location.max_lon

    def get_latlon(self):
        return str(self.latitude)+','+str(self.longitude)

    def __str__(self):
        return json.dumps({'id':self.id,'lat':self.latitude,'lon':self.longitude})