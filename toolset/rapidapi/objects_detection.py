
# Tool: objects_detection, https://rapidapi.com/ai-engine-ai-engine-default/api/objects-detection/

import os
import requests
from toolset.utils import caching, check_func_call
from toolset.utils import check_image_url


TOOL_NAME = __name__.split(".")[-1]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]


@check_func_call("rapidapi", TOOL_NAME, "objects_detection")
@caching(time_str="long term", tool_name=TOOL_NAME)
def objects_detection(args):
	url = "https://objects-detection.p.rapidapi.com/objects-detection"
	
	payload = args  # { "url": "https://openmediadata.s3.eu-west-3.amazonaws.com/birds.jpeg" }
	headers = {
	 "content-type": "application/x-www-form-urlencoded",
	 "X-RapidAPI-Key": RAPIDAPI_KEY,
	 "X-RapidAPI-Host": "objects-detection.p.rapidapi.com"
	}

	if "image" in args:
		headers = {
			# "content-type": "multipart/form-data;",
			"X-RapidAPI-Key": RAPIDAPI_KEY,
			"X-RapidAPI-Host": "objects-detection.p.rapidapi.com"
		}
		image_path = args['image']
		if not os.path.isabs(image_path):
			image_path = os.path.join(os.environ["FILE_DIR"], image_path)
		if not os.path.exists(image_path):
			raise Exception(f"File not found: {image_path}")
		files = {"image": open(image_path, 'rb')}
		# print("detected image:", args['image'])
		response = requests.post(url, files=files,  headers=headers)
	elif "url" in args:
		if not check_image_url(args['url']):
			return {"status": "error", "message": "the provided URL is not referring to an image"}
		response = requests.post(url, data=payload, headers=headers)
	else:
		return {"status": "error", "msg": "neither image file nor url was provided."}
	
	return response.json()

        