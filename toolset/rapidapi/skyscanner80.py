# https://rapidapi.com/datastore/api/skyscanner80

import requests
import os
from toolset.utils import caching, check_func_call


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]



@check_func_call("rapidapi", TOOL_NAME, "get_config")
@caching(time_str="long term", tool_name=TOOL_NAME)
def get_config(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/get-config"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()



@check_func_call("rapidapi", TOOL_NAME, "flights_auto_complete")
@caching(time_str="long term", tool_name=TOOL_NAME)
def flights_auto_complete(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"

    querystring = args  # {"query":"new","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "flights_search_one_way")
@caching(time_str="1d", tool_name=TOOL_NAME)
def flights_search_one_way(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way"

    querystring = args  # {"fromId":"eyJzIjoiTEFYQSIsImUiOiIyNzUzNjIxMSIsImgiOiIyNzUzNjIxMSJ9=","toId":"eyJzIjoiTE9ORCIsImUiOiIyNzU0NDAwOCIsImgiOiIyNzU0NDAwOCJ9","adults":"1","cabinClass":"economy","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "flights_search_roundtrip")
@caching(time_str="1d", tool_name=TOOL_NAME)
def flights_search_roundtrip(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip"

    querystring =  args # {"fromId":"eyJzIjoiTllDQSIsImUiOiIyNzUzNzU0MiIsImgiOiIyNzUzNzU0MiIsInAiOiJDSVRZIn0=","toId":"eyJzIjoiTEFYQSIsImUiOiIyNzUzNjIxMSIsImgiOiIyNzUzNjIxMSIsInAiOiJDSVRZIn0=","departDate":"2024-03-11","adults":"1","cabinClass":"economy","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


# @check_func_call("rapidapi", TOOL_NAME, "flights_search_multi_city")
@caching(time_str="1d", tool_name=TOOL_NAME)
def flights_search_multi_city(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-multi-city"

    payload = {
        "market": "IN",
        "locale": "en-GB",
        "currency": "INR",
        "adults": 1,
        "children": 0,
        "infants": 0,
        "cabinClass": "economy",
        "flights": [
            {
                "fromId": "eyJzIjoiTllDQSIsImUiOiIyNzUzNzU0MiIsImgiOiIyNzUzNzU0MiIsInAiOiJDSVRZIn0=",
                "toId": "eyJzIjoiTEFYQSIsImUiOiIyNzUzNjIxMSIsImgiOiIyNzUzNjIxMSIsInAiOiJDSVRZIn0=",
                "departDate": "2024-06-21"
            },
            {
                "fromId": "eyJzIjoiTEFYQSIsImUiOiIyNzUzNjIxMSIsImgiOiIyNzUzNjIxMSIsInAiOiJDSVRZIn0=",
                "toId": "eyJzIjoiTllDQSIsImUiOiIyNzUzNzU0MiIsImgiOiIyNzUzNzU0MiIsInAiOiJDSVRZIn0=",
                "departDate": "2024-06-28"
            }
        ]
    }
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "flights_search_everywhere")
@caching(time_str="1d", tool_name=TOOL_NAME)
def flights_search_everywhere(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-everywhere"

    querystring =  args  # {"fromId":"eyJzIjoiVFlPQSIsImUiOiIyNzU0MjA4OSIsImgiOiIyNzU0MjA4OSIsInAiOiJDSVRZIn0=","adults":"1","cabinClass":"economy","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "flights_search_incomplete")
@caching(time_str="1d", tool_name=TOOL_NAME)
def flights_search_incomplete(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-incomplete"

    querystring =  args  # {"currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "flights_flight_detail")
@caching(time_str="1d", tool_name=TOOL_NAME)
def flights_flight_detail(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/detail"

    querystring =  args  # {"currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "flights_price_calendar")
@caching(time_str="1d", tool_name=TOOL_NAME)
def flights_price_calendar(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/price-calendar"

    querystring =  args  # {"fromId":"eyJzIjoiTllDQSIsImUiOiIyNzUzNzU0MiIsImgiOiIyNzUzNzU0MiIsInAiOiJDSVRZIn0=","toId":"eyJzIjoiTEFYQSIsImUiOiIyNzUzNjIxMSIsImgiOiIyNzUzNjIxMSIsInAiOiJDSVRZIn0=","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "hotels_hotel_auto_complete")
@caching(time_str="long term", tool_name=TOOL_NAME)
def hotels_hotel_auto_complete(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/auto-complete"

    querystring =  args  # {"query":"new","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "hotels_search")
@caching(time_str="long term", tool_name=TOOL_NAME)
def hotels_search(args): 

    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/search"

    querystring = args  # {"entityId":"27539520","rooms":"1","adults":"1","resultsPerPage":"15","page":"1","priceType":"PRICE_PER_NIGHT","sorting":"-relevance","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "hotels_hotel_detail")
@caching(time_str="long term", tool_name=TOOL_NAME)
def hotels_hotel_detail(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/detail"

    querystring =  args  # {"id":"218345415","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "hotels_prices")
@caching(time_str="1d", tool_name=TOOL_NAME)
def hotels_prices(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/prices"

    querystring = {"id":"218005414","rooms":"1","adults":"2","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "hotels_reviews")
@caching(time_str="7d", tool_name=TOOL_NAME)
def hotels_reviews(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/reviews"

    querystring = {"id":"46962878","page":"1","sort":"recommended","guestType":"all","tags":"all","travellerRating":"all","dataSource":"all","filterLocale":"all"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "hotels_similar_hotels")
@caching(time_str="long term", tool_name=TOOL_NAME)
def hotels_similar_hotels(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/similar-hotels"

    querystring = args  # {"id":"218345415","rooms":"1","adults":"2","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "hotels_nearby_map")
@caching(time_str="long term", tool_name=TOOL_NAME)
def hotels_nearby_map(args):

    url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/nearby-map"

    querystring = args  # {"latitude":"19.10132","longitude":"72.8916","currency":"USD","market":"US","locale":"en-US"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()








