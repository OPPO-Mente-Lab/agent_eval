
# Tool: world_time_by_api_ninjas, https://rapidapi.com/apininjas/api/world-time-by-api-ninjas/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@caching(time_str="1m", tool_name=TOOL_NAME)
def v1_worldtime(args):
    	
	
	url = "https://world-time-by-api-ninjas.p.rapidapi.com/v1/worldtime"
	
	querystring = args  # {"city":"London"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "world-time-by-api-ninjas.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()

        