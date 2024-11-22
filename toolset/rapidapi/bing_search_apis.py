
# Tool: bing_search_apis, https://rapidapi.com/quangphatc3/api/bing-search-apis/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@caching(time_str="long term", tool_name=TOOL_NAME)
def web_search_api(args):
    	
	
	url = "https://bing-search-apis.p.rapidapi.com/api/rapid/web_search"
	
	querystring = args  # {"keyword":"how-to-use-excel-for-free","page":"0","size":"30"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "bing-search-apis.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "images_search")
@caching(time_str="long term", tool_name=TOOL_NAME)
def images_search(args):
    	
	
	url = "https://bing-search-apis.p.rapidapi.com/api/rapid/image_search"
	
	querystring = args  # {"keyword":"wallpapers","page":"0","size":"30"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "bing-search-apis.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()


def emails_search(args):
    	
	
	url = "https://bing-search-apis.p.rapidapi.com/api/rapid/email_search"
	
	querystring = args  # {"keyword":"sun"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "bing-search-apis.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)
	
	return response.json()

        