
# https://rapidapi.com/iq.faceok/api/ocr-extract-text

import os
import requests
from toolset.utils import caching, check_func_call
from toolset.utils import check_image_url


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "extract_text_from_image_url")
@caching(time_str="long term", tool_name=TOOL_NAME)
def extract_text_from_image_url(args):
    url = "https://ocr-extract-text.p.rapidapi.com/ocr"

    if not check_image_url(args['url']):
	    return {"status": "error", "message": "the provided URL is not referring to an image"}

    querystring =  args  # {"url":"https://qph.cf2.quoracdn.net/main-qimg-60dad75c0dddf8f4aa1a95040d7c3ca5-pjlq"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "ocr-extract-text.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@check_func_call("rapidapi", TOOL_NAME, "extract_text_from_image_file")
@caching(time_str="long term", tool_name=TOOL_NAME)
def extract_text_from_image_file(args):
    url = "https://ocr-extract-text.p.rapidapi.com/ocr"

    # payload = { "image": "" }
    image_path = args['image']
    if not os.path.isabs(image_path):
        image_path = os.path.join(os.environ["FILE_DIR"], image_path)
    if not os.path.exists(image_path):
        raise Exception(f"File not found: {image_path}")
    files = {"image": open(image_path, 'rb')}
	
    headers = {
        "x-rapidapi-key": "d2fb22ad1fmsh821e706dc2eeaadp16b596jsnb6b1fb983adb",
        "x-rapidapi-host": "ocr-extract-text.p.rapidapi.com",
        "Accept": "application/json",
    }
    response = requests.post(url, headers=headers, files=files)
    return response.json()

