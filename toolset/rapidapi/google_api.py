
# https://rapidapi.com/rphrp1985/api/google-api31

import requests
import os
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "video_search")
@caching(time_str="long term", tool_name=TOOL_NAME)
def video_search(args):

    url = "https://google-api31.p.rapidapi.com/videosearch"

    payload =  {
        "text":  args.get("text"),  # "Justin Bieber",
        "safesearch": args.get("safesearch", "moderate"),  # on , off
        "timelimit": "",
        "duration": "",
        "resolution": "",
        "region": args.get("region", "wt-wt"),
        "max_results": args.get("max_results", 20)
    }
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "google-api31.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()



