
# Tool: weatherapi_com, https://rapidapi.com/weatherapi/api/weatherapi-com/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]

@check_func_call("rapidapi", TOOL_NAME, "realtime_weather_api")
@caching(time_str="1h", tool_name=TOOL_NAME)
def realtime_weather_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/current.json"
	
	querystring = args  # {"q":"53.1,-0.13"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "forecast_weather_api")
@caching(time_str="12h", tool_name=TOOL_NAME)  
def forecast_weather_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
	
	querystring = args  # {"q":"London","days":"3"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "ip_lookup_api")
@caching(time_str="long term", tool_name=TOOL_NAME)
def ip_lookup_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/ip.json"
	
	querystring = args  # {"q":"<REQUIRED>"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "time_zone_api")
@caching(time_str="long term", tool_name=TOOL_NAME)
def time_zone_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/timezone.json"
	
	querystring = args  # {"q":"<REQUIRED>"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "astronomy_api")
@caching(time_str="1d", tool_name=TOOL_NAME)  
def astronomy_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/astronomy.json"
	
	querystring = args  # {"q":"London"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


# @check_func_call("rapidapi", TOOL_NAME, "history_weather_api")
@caching(time_str="long term", tool_name=TOOL_NAME)
def history_weather_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/history.json"
	
	querystring = args  # {"q":"London","dt":"<REQUIRED>","lang":"en"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "search_autocomplete_api")
@caching(time_str="long term", tool_name=TOOL_NAME)
def search_autocomplete_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/search.json"
	
	querystring = args  # {"q":"<REQUIRED>"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()

        
def sports_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/sports.json"
	
	querystring = args  # {"q":"London"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


# @check_func_call("rapidapi", TOOL_NAME, "future_weather_api")
@caching(time_str="1d", tool_name=TOOL_NAME)  
def future_weather_api(args):
    	
	
	url = "https://weatherapi-com.p.rapidapi.com/future.json"
	
	querystring = args  # {"q":"London","dt":"2022-12-25"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()

        