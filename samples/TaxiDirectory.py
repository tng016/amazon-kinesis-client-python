import Geohash
import math

class TaxiLocation:
	mlat_per_deg = 1.11E+05
	mlon_per_deg = 7.87E+04

	def __init__(self, lat, lon):
		self.lat = lat
		self.lon = lon
		self.geohash = Geohash.encode(lat,lon,precision = 6)
		self.dist_travel = 0

	def update(self,new_lat,new_lon):
		self.dist_travel += self.calc_dist(new_lat,new_lon)
		self.lat = new_lat
		self.lon = new_lon
		self.geohash = Geohash.encode(new_lat,new_lon,precision = 6)

	def calc_dist(self,new_lat,new_lon):
		v_d = abs(new_lat-self.lat)*TaxiLocation.mlat_per_deg
		h_d = abs(new_lon-self.lon)*TaxiLocation.mlon_per_deg
		return math.sqrt(v_d**2 + h_d**2)

class TaxiDirectory:
	d = {}

	@staticmethod
	def put(id,lat,lon):
		if id in TaxiDirectory.d.keys():
			TaxiDirectory.d[id].update(lat,lon)
		else:
			TaxiDirectory.d[id] = TaxiLocation(lat,lon)

	@staticmethod
	def aggregate():
		res = {}
		for key in TaxiDirectory.d.keys():
			obj = TaxiDirectory.d[key]
			if obj.geohash in res:
				res[obj.geohash][0] += 1
				res[obj.geohash][1] += obj.dist_travel
			else:
				res[obj.geohash] = [1,obj.dist_travel]
		TaxiDirectory.d = {}
		return res

# if __name__== "__main__":
# 	TaxiDirectory.put(1,40.7165036056,-73.9190213114)
# 	TaxiDirectory.put(1,40.7356258347,-73.9022453005)
# 	TaxiDirectory.put(2,40.7165036056,-73.9190213114)
# 	TaxiDirectory.put(2,40.7356258347,-73.9022453005)
# 	print(TaxiDirectory.d[1].lat,TaxiDirectory.d[1].lon,TaxiDirectory.d[1].geohash,TaxiDirectory.d[1].dist_travel)
# 	print(TaxiDirectory.aggregate())