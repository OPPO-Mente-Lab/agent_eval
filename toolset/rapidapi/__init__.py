
import os
import json

# == import tools ==
from . import airports
from . import currency_exchange
from . import geocoding_by_api_ninjas
from . import google_translate
from . import ip_geo_location
from . import list_of_all_countries_and_languages_with_their_codes
from . import news_api
from . import onecompiler_apis
from . import public_holiday
from . import weatherapi_com
from . import web_capture
from . import world_time_by_api_ninjas
from . import recipe_by_api_ninjas
from . import objects_detection
from . import ocr_extract_text
from . import bing
from . import bing_search_apis
from . import google_api
from . import tourist_attraction
from . import skyscanner80
# == END - import tools ==



class RapidAPI():
    def __init__(self, tools_to_use:list):
        self.tools_to_use = tools_to_use
        self.tool_docs, self.api_docs = self.get_docs()

    def __call__(self, tool_name, api_name, args):
        if tool_name not in self.tool_docs:
            return {"status": "error", "message": f"The tool {tool_name} is not found in our current RapidAPI toolset."}
        elif api_name not in self.api_docs[tool_name]:
            return {"status": "error", "message": f"{api_name} is not an API of {tool_name} in our current RapidAPI toolset."}
            
        try:
            # result = _route_mapping[tool_name][api_name](args)
            # module_name = getattr(sys.modules[__name__], "tool_name") 
            module_name = globals().get(tool_name)
            func_name = getattr(module_name, api_name)
            result = func_name(args)
            if isinstance(result, dict):
                return result
            ret = {"status": "ok", "data": result}
        except Exception as e:
            ret = {"status": "error", "msg": str(e), "data": None}
        return ret


    def get_docs(self):
        doc_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "docs") 
        fn_name_list = os.listdir(doc_dir)

        tool_docs = {}
        api_docs = {}
        # for name in fn_name_list:
        for name in self.tools_to_use:
            full_fn = os.path.join(doc_dir, name+".json")
            try:
                with open(full_fn) as file:
                    doc = json.loads(file.read())
                tool_name = doc["tool_name"]
                tool_docs[tool_name] = doc
                api_docs[tool_name] = {}
                for api in doc["APIs"]:
                    api_name = api["function"]['name']
                    api_docs[tool_name][api_name] = api['function']
            except Exception as e:
                print(e)
        return tool_docs, api_docs
    

