

# Tool: web_capture, https://rapidapi.com/abdheshnayak/api/web-capture2

import os
import requests
import time
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]

RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "take_image_screenshot")
@caching(time_str="long term", tool_name=TOOL_NAME)
def take_image_screenshot(args):
	url = "https://web-capture2.p.rapidapi.com/image"
	
	querystring = args  # {"url":"https://google.com","height":"780","width":"1024"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "web-capture2.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)

	# print(response.headers['content-type'])

	output_dir = os.path.join(os.path.dirname(__file__), "../tool_output/")
	# name, ext = os.path.splitext(os.path.basename(path))
	name = args["url"].replace("/", "_").replace(":", "#") 
	file_name = name + '_capture.jpeg'
	output_path = os.path.join(output_dir, file_name)
	with open(output_path, "wb") as f:
		f.write(response.content)
	return {'output_image_path': output_path, 'status': 'success'}
	
	# return response.json()


# @check_func_call("rapidapi", TOOL_NAME, "generate_pdf")
@caching(time_str="long term", tool_name=TOOL_NAME)
def generate_pdf(args):
    	
	
	url = "https://web-capture2.p.rapidapi.com/pdf"
	
	querystring = args  # {"url":"https://google.com","height":"780","width":"1024"}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "web-capture2.p.rapidapi.com"
	}
	
	response = requests.get(url, headers=headers, params=querystring)

	output_dir = os.path.join(os.path.dirname(__file__), "../tool_output/")
	# name, ext = os.path.splitext(os.path.basename(path))
	name = args["url"].replace("/", "_").replace(":", "#") 
	file_name = name + '.pdf'
	output_path = os.path.join(output_dir, file_name)
	with open(output_path, "wb") as f:
		f.write(response.content)
	return {'output_image_path': output_path, 'status': 'success'}
	
	# return response.json()


@caching(time_str="long term", tool_name=TOOL_NAME)
def get_pdf_from_html(args):
	
	url = "https://web-capture2.p.rapidapi.com/pdf"
	
	querystring = args  # {"height":"780","width":"1024"}
	payload = {"html": args["html"]}
	
	headers = {
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "web-capture2.p.rapidapi.com"
	}
	
	response = requests.post(url, headers=headers, params=querystring, json=payload)

	output_dir = os.path.join(os.path.dirname(__file__), "../tool_output/")
	# name, ext = os.path.splitext(os.path.basename(path))
	file_name = f'html_{int(time.time()*1e6)}.pdf'
	output_path = os.path.join(output_dir, file_name)
	with open(output_path, "wb") as f:
		f.write(response.content)
	return {'output_image_path': output_path, 'status': 'success'}
	
	# return response.json()

        