import Geohash
import math

class TaxiLocation:
	mlat_per_deg = 1.11E+05
	mlon_per_deg = 7.87E+04

	def __init__(self, lat, lon):
		self.lat = lat
		self.lon = lon
		self.geohash = Geohash.encode(lat,lon,precision = 6)

	def update(self,new_lat,new_lon):
		self.lat = new_lat
		self.lon = new_lon
		self.geohash = Geohash.encode(new_lat,new_lon,precision = 6)

	def calc_dist(self,new_lat,new_lon):
		v_d = abs(new_lat-self.lat)*TaxiLocation.mlat_per_deg
		h_d = abs(new_lon-self.lon)*TaxiLocation.mlon_per_deg
		return math.sqrt(v_d**2 + h_d**2)

class TaxiDirectory:
	d = {}
	hashes = {} #geohash map to total_dist, count of entries, count of cars

	@staticmethod
	def put(id,lat,lon):
		if id in TaxiDirectory.d.keys():
			loc =TaxiDirectory.d[id]
			dist = loc.calc_dist(lat,lon)
			loc.update(lat,lon)
			if dist < 150:
				if loc.geohash in TaxiDirectory.hashes.keys():
					TaxiDirectory.hashes[loc.geohash][0] += dist
					TaxiDirectory.hashes[loc.geohash][1] += 1
				else:
					TaxiDirectory.hashes[loc.geohash] = [dist,1,0]
		else:
			TaxiDirectory.d[id] = TaxiLocation(lat,lon)

	@staticmethod
	def aggregate():
		for key in TaxiDirectory.d.keys():
			obj = TaxiDirectory.d[key]
			if obj.geohash in TaxiDirectory.hashes.keys():
				TaxiDirectory.hashes[obj.geohash][2] += 1
		res = TaxiDirectory.hashes
		TaxiDirectory.d = {}
		TaxiDirectory.hashes = {}
		return res

# if __name__== "__main__":
# 	TaxiDirectory.put(1,40.7165036056,-73.9190213114)
# 	TaxiDirectory.put(1,40.7166036056,-73.9191213114)
# 	TaxiDirectory.put(1,40.7167036056,-73.9192213114)
# 	TaxiDirectory.put(2,41.7167036056,-73.9192213114)
# 	TaxiDirectory.put(2,41.7168036056,-73.9193213114)
# 	TaxiDirectory.put(3,41.7167036056,-73.9192213114)
# 	TaxiDirectory.put(3,41.7168036056,-73.9193213114)
# 	print(TaxiDirectory.d)
# 	print(TaxiDirectory.hashes)
# 	print(TaxiDirectory.aggregate())