
# Tool: tourist_attraction, https://rapidapi.com/ptwebsolution/api/tourist-attraction/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "currencies")
@caching(time_str="long term", tool_name=TOOL_NAME) 
def currencies(args):
    	
	
	url = "https://tourist-attraction.p.rapidapi.com/currencies"
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "tourist-attraction.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "languages")
@caching(time_str="long term", tool_name=TOOL_NAME)
def languages(args):
    	
	
	url = "https://tourist-attraction.p.rapidapi.com/languages"
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "tourist-attraction.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "typeahead")
@caching(time_str="long term", tool_name=TOOL_NAME)
def typeahead(args):
    	
	
	url = "https://tourist-attraction.p.rapidapi.com/typeahead"
	
	payload = args  # {"q": "las", "language": "en_US"}
	headers = {
	 "content-type": "application/x-www-form-urlencoded",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "tourist-attraction.p.rapidapi.com"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "search")
@caching(time_str="long term", tool_name=TOOL_NAME)
def search(args):
    	
	
	url = "https://tourist-attraction.p.rapidapi.com/search"
	
	payload = args  # {"location_id": "45963", "language": "en_US", "currency": "USD", "offset": "0"}
	headers = {
	 "content-type": "application/x-www-form-urlencoded",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "tourist-attraction.p.rapidapi.com"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "detail")
@caching(time_str="long term", tool_name=TOOL_NAME)
def detail(args):
    	
	
	url = "https://tourist-attraction.p.rapidapi.com/detail"
	
	payload = args  # {"location_id": "8797440", "language": "en_US", "currency": "USD"}
	headers = {
	 "content-type": "application/x-www-form-urlencoded",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "tourist-attraction.p.rapidapi.com"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "photos")
@caching(time_str="30d", tool_name=TOOL_NAME)
def photos(args):
    	
	
	url = "https://tourist-attraction.p.rapidapi.com/photos"
	
	payload = args  # {"location_id": "8797440", "language": "en_US", "currency": "USD", "offset": "0"}
	if "language" not in payload:
		payload['language'] = 'en_US'
	if "currency" not in payload:
		payload["currency"] == "USD"

	headers = {
	 "content-type": "application/x-www-form-urlencoded",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "tourist-attraction.p.rapidapi.com"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "reviews")
@caching(time_str="7d", tool_name=TOOL_NAME)
def reviews(args):
    	
	
	url = "https://tourist-attraction.p.rapidapi.com/reviews"
	
	payload = args  # {"location_id": "8797440", "language": "en_US", "currency": "USD", "offset": "0"}
	if "currency" not in payload:
		payload["currency"] == "USD"
		
	headers = {
	 "content-type": "application/x-www-form-urlencoded",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "tourist-attraction.p.rapidapi.com"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	
	return response.json()

    