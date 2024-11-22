import re
from datetime import timedelta
from typing import Hashable
import os
import pickle
import time
import json
import requests



def _parse_timedelta_from_str(time_str:str): # format: '2d12h20m9s'
    regex = re.compile(r'((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?')
    parts = regex.match(time_str)
    parts = parts.groupdict()
    parts_conv = {}
    for k,v in parts.items():
        v_conv = int(v) if v is not None else 0
        parts_conv[k] = v_conv
    td = timedelta(**parts_conv)
    return td


def _make_hashable(inst):

    if type(inst) == list:
        for i in range(len(inst)):
            if not isinstance(inst[i], Hashable):
                inst[i] = _make_hashable(inst[i])
        inst = tuple(inst)
    elif type(inst) == dict:
        for k,v in inst.items():
            if not isinstance(v, Hashable):
                inst[k] = _make_hashable(v)
        inst = tuple(sorted(list(inst.items())))
    elif type(inst) == set:
        inst = list(inst)
        inst = _make_hashable(inst)
    return inst



def caching(time_str="long term", tool_name=None):  # format: '2d12h20m9s' or "long term"
    
    def wrapper(func):
        cache_dir = os.path.join(os.path.dirname(__file__), ".cache/")
        os.makedirs(cache_dir, exist_ok=True)
        if time_str.lower() == "long term":
            cache_duration = timedelta(days=100000)
        else:
            cache_duration = _parse_timedelta_from_str(time_str)
        cache_fn = os.path.join(cache_dir, ('' if tool_name is None else (tool_name+'.')) + func.__name__ + ".pkl")
        if os.path.exists(cache_fn):
            with open(cache_fn, "rb") as file:
                cache_obj = pickle.load(file)
        else:
            cache_obj = {"stats": {"request_count": 0, "use_cache_count": 0}}

        def inner(args):
            print(f"=> Excuting tool `{tool_name}/{func.__name__}` with args: {json.dumps(args, ensure_ascii=False)}")
            hashable_args = _make_hashable(args)
            res_in_cache = cache_obj.get(hashable_args, None)
            if res_in_cache is not None:
                # print(res_in_cache)
                create_time = res_in_cache["create_time"]
                cur_time = time.time()
                td = timedelta(seconds=cur_time-create_time)
                if td < cache_duration:
                    cache_obj["stats"]["use_cache_count"] += 1
                    with open(cache_fn, "wb") as file:
                        pickle.dump(cache_obj, file)
                    print("Use result in cache.")
                    # print(res_in_cache)
                    return res_in_cache["data"]
            try:
                res = func(args)
                cache_obj["stats"]["request_count"] += 1
            except Exception as e:
                print("<= Fail. Exception occurs (thrown from caching)", e)
                return {"status": "failed", "message": "the tool crashed. check whether you have passed valid parameters."}
            
            res_str = json.dumps(res, ensure_ascii=False).lower()
            if "you have exceeded the monthly quota" in res_str:
                return res
            
            cache_obj[hashable_args] = {"data": res, "create_time": time.time()}
            with open(cache_fn, "wb") as file:
                pickle.dump(cache_obj, file)
                print("<= Succeed. Cache updated.")
            return res
        
        return inner

    return wrapper





def read_docs(tool_src):
    doc_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), tool_src, "docs") 
    fn_name_list = os.listdir(doc_dir)

    tool_docs = {}
    api_docs = {}
    for name in fn_name_list:
        full_fn = os.path.join(doc_dir, name)
        with open(full_fn) as file:
            doc = json.loads(file.read())
        tool_name = doc["tool_name"]
        tool_docs[tool_name] = doc
        api_docs[tool_name] = {}
        for api in doc["APIs"]:
            api_name = api["function"]['name']
            api_docs[tool_name][api_name] = api['function']
    return tool_docs, api_docs

_, rapidapi_api_docs = read_docs("rapidapi")
_, devtools_api_docs = read_docs("dev_tools")

def check_func_call(tool_src, tool_name, api_name):

    def wrapper(func):
        if tool_src == "rapidapi":
            api_docs = rapidapi_api_docs
        elif tool_src == "dev_tools":
            api_docs = devtools_api_docs
        
        api_doc = api_docs[tool_name][api_name]

        def inner_func(args):
            # check required parameters
            for p in api_doc['parameters']['required']:
                if p not in args:
                    return {"status": 'error', "message": f"required parameter `{p}` is not provided."}
            
            return func(args)

        return inner_func

    return wrapper




def check_image_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    if "image" in resp.headers.get('content-type'):
        return True
    else:
        return False

