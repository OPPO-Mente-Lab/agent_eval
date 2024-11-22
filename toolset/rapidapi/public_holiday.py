
# Tool: public_holiday, https://rapidapi.com/theapiguy/api/public-holiday/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "public_holidays")
@caching(time_str="long term", tool_name=TOOL_NAME)
def public_holidays(args):
    	
	
	url = f"https://public-holiday.p.rapidapi.com/{args['Year']}/{args['CountryCode']}"
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "public-holiday.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()

        