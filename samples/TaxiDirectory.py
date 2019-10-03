import Geohash
import math
import json

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

	def __str__(self):
		return json.dumps({'lat':self.lat,'lon':self.lon,'geohash':self.geohash})

class TaxiDirectory:
	def __init__(self):
		self.d = {}
		self.hashes = {} #geohash map to total_dist, count of entries, count of cars

	def put(self,id,lat,lon):
		if id in self.d.keys():
			loc =self.d[id]
			dist = loc.calc_dist(lat,lon)
			loc.update(lat,lon)
			if dist < 200:
				if loc.geohash in self.hashes.keys():
					self.hashes[loc.geohash][0] += dist
					self.hashes[loc.geohash][1] += 1
				else:
					self.hashes[loc.geohash] = [dist,1,0]
		else:
			self.d[id] = TaxiLocation(lat,lon)

	def aggregate(self):
		for key in self.d.keys():
			obj = self.d[key]
			if obj.geohash in self.hashes.keys():
				self.hashes[obj.geohash][2] += 1
		res = self.hashes
		self.d = {}
		self.hashes = {}
		return res

	def __str__(self):
		s = 'd: {'
		for key in self.d:
			s += str(key) +':' + str(self.d[key])
		return s + '} \nhashes:' + json.dumps(self.hashes)
