import numpy as np
import random
import geohash2 as Geohash
from TaxiDirectory import TaxiDirectory
from Taxi_Location import Taxi_Location

if __name__== "__main__":

    taxis = []
    for i in range(10):
        taxis.append(Taxi_Location())
    
    directory = TaxiDirectory()
    for i in range(10):
        for t in taxis:
            t.randomise()
            directory.put(t.id,t.latitude,t.longitude)
    a = directory.aggregate()

    for i in range(10):
        for t in taxis:
            t.randomise()
            directory.put(t.id,t.latitude,t.longitude)
    b = directory.aggregate()
    print(a)
    print(b)