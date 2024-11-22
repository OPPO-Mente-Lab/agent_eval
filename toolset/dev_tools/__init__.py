
import os
import json

## import tools
from . import access_user_info
from . import agent_equipments
from . import calculator
from . import image_processing
from . import image_remove_bg
from . import image_translation
from . import calendar


class DevTools():
    def __init__(self, tools_to_use:list):
        self.tools_to_use = tools_to_use
        self.tool_docs, self.api_docs = self.get_docs()

    def __call__(self, tool_name, api_name, args):
        if tool_name not in self.tool_docs:
            return {"status": "error", "message": f"The tool {tool_name} is not found in our current DevTools toolset."}
        elif api_name not in self.api_docs[tool_name]:
            return {"status": "error", "message": f"{api_name} is not an API of {tool_name} in our current DevTools toolset."}

        try:
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
    



