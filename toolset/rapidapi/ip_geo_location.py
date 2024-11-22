
# Tool: ip_geo_location, https://rapidapi.com/natkapral/api/ip-geo-location/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "visitor_lookup")
@caching(time_str="long term", tool_name=TOOL_NAME)
def visitor_lookup(args):
    	
	
	url = "https://ip-geo-location.p.rapidapi.com/ip/check"
	
	querystring = args  # {"format":"json"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "ip-geo-location.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "ip_lookup")
@caching(time_str="long term", tool_name=TOOL_NAME)
def ip_lookup(args):
    	
	
	url = f"https://ip-geo-location.p.rapidapi.com/ip/{args['ip']}"
	
	querystring = args  # {"format":"json"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "ip-geo-location.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()

        