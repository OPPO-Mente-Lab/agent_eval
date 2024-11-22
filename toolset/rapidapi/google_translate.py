
# Tool: google_translate, https://rapidapi.com/googlecloud/api/google-translate1/

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "detect")
@caching(time_str="long term", tool_name=TOOL_NAME)
def detect(args):
    	
	
	url = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"
	
	payload =  args  # { "q": "English is hard, but detectably so" }
	headers = {
	 "content-type": "application/x-www-form-urlencoded",
	 "Accept-Encoding": "application/gzip",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "languages")
@caching(time_str="long term", tool_name=TOOL_NAME)
def languages(args):
    	
	
	url = "https://google-translate1.p.rapidapi.com/language/translate/v2/languages"
	
	headers = {
	 "Accept-Encoding": "application/gzip",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers)
	
	return response.json()


@check_func_call("rapidapi", TOOL_NAME, "translate")
@caching(time_str="long term", tool_name=TOOL_NAME)
def translate(args):
    	
	
	url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
	
	payload =  args  
	headers = {
	 "content-type": "application/x-www-form-urlencoded",
	 "Accept-Encoding": "application/gzip",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	
	return response.json()

        