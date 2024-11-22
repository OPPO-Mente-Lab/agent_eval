
# https://rapidapi.com/Glavier/api/bing23

import requests
import os
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "web_search")
@caching(time_str="long term", tool_name=TOOL_NAME)
def web_search(args):
    url = "https://bing23.p.rapidapi.com/v1/web-search"

    querystring = args  # {"query":"ChatGPT","offset":"0","language":"en"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "bing23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()



