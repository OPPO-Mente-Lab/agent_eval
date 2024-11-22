
# Tool: list_of_all_countries_and_languages_with_their_codes, https://rapidapi.com/contactteamrkg/api/list-of-all-countries-and-languages-with-their-codes

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@caching(time_str="long term", tool_name=TOOL_NAME)
def list_of_all_countries(args):
    	
	
	url = "https://list-of-all-countries-and-languages-with-their-codes.p.rapidapi.com/countries"
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "list-of-all-countries-and-languages-with-their-codes.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()


@caching(time_str="long term", tool_name=TOOL_NAME)
def list_of_all_languages(args):
    	
	
	url = "https://list-of-all-countries-and-languages-with-their-codes.p.rapidapi.com/languages"
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "list-of-all-countries-and-languages-with-their-codes.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()

        