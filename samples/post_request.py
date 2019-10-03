# importing the requests library 
import requests 

def post_to_app(data):
	# defining the api-endpoint  
	API_ENDPOINT = "http://localhost:3000/populate"
	  
	# your API key here 
	# API_KEY = "XXXXXXXXXXXXXXXXX"

	# data to be sent to api 
	# data = {'surge[supply]':1,
	#         'surge[demand]':2, 
	#         'surge[geohash]':'abcd123', 
	#         'surge[congestion]':0.5} 
	# data = {"eventType": "AAS_PORTAL_START", "data": {"uid": "hfe3hf45huf33545", "aid": "1", "vid": "1"}}
	processed_data = {'surge': data}
	# sending post request and saving response as response object 
	try:
		r = requests.post(url = API_ENDPOINT, json = processed_data) 
		# extracting response text  
		return(r.status_code)
	except requests.exceptions.RequestException as e:
		return("Post to application failed. Exception was" + e)
  
