
# Tool: airports, https://rapidapi.com/epsi/api/airports15/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@caching(time_str="30d", tool_name=TOOL_NAME)
def query_airports_by_name(args):
    	
	
	url = "https://airports15.p.rapidapi.com/airports"
	
	querystring = args  # {"name":"Singapore","page":"1","page_size":"20","sorted_by":"icao"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "airports15.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@caching(time_str="30d", tool_name=TOOL_NAME)
def get_airport_by_iata_code(args):
    	
	
	url = f"https://airports15.p.rapidapi.com/airports/iata/{args['iata_code']}"
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "airports15.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()


@caching(time_str="30d", tool_name=TOOL_NAME)
def get_airport_by_icao_code(args):
    	
	
	url = f"https://airports15.p.rapidapi.com/airports/icao/{args['icao_code']}"
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "airports15.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()

        