import numpy as np
import random
import geohash2 as Geohash
from TaxiDirectory import TaxiDirectory
from Taxi_Location import Taxi_Location
import post_request

if __name__== "__main__":

    taxis = []
    for i in range(1000):
        taxis.append(Taxi_Location())
    
    directory = TaxiDirectory()
    for i in range(60):
        for t in taxis:
            t.randomise()
            directory.put(t.id,t.latitude,t.longitude)
    a = directory.aggregate()
    print(a)
    print(post_request.post_to_app(a))