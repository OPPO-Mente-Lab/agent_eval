# Tool: onecompiler_apis, https://rapidapi.com/onecompiler-onecompiler-default/api/onecompiler-apis

import os
import requests
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "execute_code")
@caching(time_str="long term", tool_name=TOOL_NAME)
def execute_code(args): # content: str

	url = "https://onecompiler-apis.p.rapidapi.com/api/v1/run"

	content = args['content']
	payload = {
		"language": "python",
		"stdin": "",
		"files": [
			{
				"name": "index.py",
				"content": content
			}
		]
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": RAPIDAPI_KEY,
		"X-RapidAPI-Host": "onecompiler-apis.p.rapidapi.com"
	}

	response = requests.post(url, json=payload, headers=headers)

	return response.json()