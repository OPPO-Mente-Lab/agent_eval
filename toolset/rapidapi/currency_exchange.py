
# Tool: currency_exchange, https://rapidapi.com/fyhao/api/currency-exchange/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@caching(time_str="long term", tool_name=TOOL_NAME)
def listquotes(args):
    	
	
	url = "https://currency-exchange.p.rapidapi.com/listquotes"
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()


@caching(time_str="7d", tool_name=TOOL_NAME)
def exchange(args):
    	
	
	url = "https://currency-exchange.p.rapidapi.com/exchange"
	
	querystring = args  # {"from":"SGD","to":"MYR","q":"1.0"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()

        