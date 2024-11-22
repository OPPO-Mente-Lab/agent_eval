import os
import yaml
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yml")) as file:
    ENV_CONFIG = yaml.safe_load(file)

os.environ["RAPIDAPI_KEY"] = ENV_CONFIG["X-RapidAPI-Key"]
if ENV_CONFIG["FILE_DIR"] == "":
    file_parent_dir = os.environ["FILE_DIR"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/")
    if not os.path.exists(os.path.join(file_parent_dir, "files")):
        raise Exception("The parent directory of files/ is not set yet. Set it in toolset/config.yml first.")
else:
    os.environ["FILE_DIR"] = ENV_CONFIG["FILE_DIR"]

from .rapidapi import RapidAPI
from .dev_tools import DevTools


class Toolset:
    def __init__(self):
        self.rapidapi_tools_names = ENV_CONFIG.get("RAPIDAPI_TOOLS") or []
        self.dev_tools_names = ENV_CONFIG.get("DEV_TOOLS") or []
        self.rapidapi = RapidAPI(self.rapidapi_tools_names)
        self.dev_tools = DevTools(self.dev_tools_names)


    def call_tool(self, tool_name, api_name, args):
        if tool_name in self.rapidapi_tools_names:
            return self.rapidapi(tool_name, api_name, args)
        elif tool_name in self.dev_tools_names:
            return self.dev_tools(tool_name, api_name, args)
        else:
            return {"status": "error", "message": f"The tool named {tool_name} is not included in current toolset."}

    def get_api_docs(self):
        all_docs = {}
        all_docs.update(self.rapidapi.api_docs)
        all_docs.update(self.dev_tools.api_docs)
        return all_docs


