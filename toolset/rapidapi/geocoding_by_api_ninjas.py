
# Tool: geocoding_by_api_ninjas, https://rapidapi.com/apininjas/api/geocoding-by-api-ninjas

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@caching(time_str="long term", tool_name=TOOL_NAME)
def v1_geocoding(args):
    	
	
	url = "https://geocoding-by-api-ninjas.p.rapidapi.com/v1/geocoding"
	
	querystring = args  # {"city":"Seattle"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "geocoding-by-api-ninjas.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@caching(time_str="long term", tool_name=TOOL_NAME)
def v1_reversegeocoding(args):
    	
	
	url = "https://geocoding-by-api-ninjas.p.rapidapi.com/v1/reversegeocoding"
	
	querystring = args  # {"lat":"47.6062","lon":"-122.3321"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "geocoding-by-api-ninjas.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()

        