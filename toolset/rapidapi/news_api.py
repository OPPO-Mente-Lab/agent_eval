
# Tool: news_api, https://rapidapi.com/bonaipowered/api/news-api14

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "top_headlines")
@caching(time_str="1d", tool_name=TOOL_NAME)
def top_headlines(args):
    	
	
	url = "https://news-api14.p.rapidapi.com/top-headlines"
	
	querystring = args  # {"country":"us","language":"en","pageSize":"10","category":"sports"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "news-api14.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "top_headlines")
@caching(time_str="7d", tool_name=TOOL_NAME)
def search(args):
    	
	
	url = "https://news-api14.p.rapidapi.com/search"
	
	querystring = args  # {"q":"computer","country":"us","language":"en","pageSize":"10","publisher":"cnn.com,bbc.com"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "news-api14.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()

        