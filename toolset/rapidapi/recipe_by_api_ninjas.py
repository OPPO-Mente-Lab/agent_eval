
# https://rapidapi.com/apininjas/api/recipe-by-api-ninjas

import requests
from toolset.utils import caching, check_func_call
import os


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "v1_recipe")
@caching(time_str="long term", tool_name=TOOL_NAME)
def v1_recipe(args):
    
    url = "https://recipe-by-api-ninjas.p.rapidapi.com/v1/recipe"

    querystring = args  # {"query":"italian wedding soup"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "recipe-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()




