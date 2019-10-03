# importing the requests library 
import requests 
import json

def post_to_app(data):
	# defining the api-endpoint  
	API_ENDPOINT = "http://grabassignment-env-1.ea33qnuunt.us-west-1.elasticbeanstalk.com/populate"
	  
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
		headers = {'content-type': 'application/json'}
		r = requests.post(url = API_ENDPOINT, data=json.dumps(processed_data), headers=headers) 
		# extracting response text  
		return(r.status_code)
	except requests.exceptions.RequestException as e:
		return("Post to application failed. Exception was" + e)
  
