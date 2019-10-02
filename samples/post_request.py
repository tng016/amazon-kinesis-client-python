# importing the requests library 
import requests 
  
# defining the api-endpoint  
API_ENDPOINT = "http://localhost:3000/surges"
  
# your API key here 
# API_KEY = "XXXXXXXXXXXXXXXXX"
  
# your source code here 
# source_code = ''' 
# print("Hello, world!") 
# a = 1 
# b = 2 
# print(a + b) 
# '''
  
# data to be sent to api 
data = {'surge[supply]':1,
        'surge[demand]':2, 
        'surge[geohash]':'abcd123', 
        'surge[congestion]':0.5} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url) 