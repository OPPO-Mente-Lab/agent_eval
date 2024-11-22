
import sys 
from toolset import Toolset
import os
import pandas as pd
from tqdm.auto import tqdm
import json
from copy import deepcopy
import pickle


from openai_config import client  # replace it with other llms as per your need in evaluation


toolset = Toolset()
api_docs = toolset.get_api_docs()

# query_airports_by_name, web_search, days_of_month, ip_lookup, search
def convert_doc_to_openai_format(doc):
    new_doc = deepcopy(doc)
    for k in new_doc["parameters"]['properties']:
        new_doc["parameters"]['properties'][k]["type"] = param_dt = new_doc["parameters"]['properties'][k]["type"].lower()
        if param_dt not in ["string", "number", "integer", "object", "array", "boolean", "null"]:
            # STRING, INT, ENUM, DATE (YYYY-MM-DD)
            if param_dt in ["int"]:
                new_doc["parameters"]['properties'][k]["type"] = "integer"
            else:
                new_doc["parameters"]['properties'][k]["type"] = "string"
    # new_doc = {"type": "function", "function": new_doc}
    return new_doc



def perform_task1(tool_name, api_name, instruction, llm_name="gpt-4-8k"):

    api_doc = convert_doc_to_openai_format(api_docs[tool_name][api_name]) 
    api_doc_list = [api_doc]

    conv = [{"role": "user", "content": instruction}]

    chat_completion = client.chat.completions.create(
        model=llm_name,  # "gpt-3.5-turbo"
        messages=conv,
        stream=False,
        functions=api_doc_list
    )

    msg = chat_completion.choices[0].message
    msg = msg.model_dump()
    conv.append(msg)
    return conv 



def perform_task2(tool_name, api_name, instruction, simi_api_list, simi_api_num=5, llm_name="gpt-4-8k"):

    api_doc = convert_doc_to_openai_format(api_docs[tool_name][api_name]) 
    api_doc_list = [api_doc]

    for simi_tool, simi_api in simi_api_list[:simi_api_num]:
        api_doc = convert_doc_to_openai_format(api_docs[simi_tool][simi_api]) 
        api_doc_list.append(api_doc)

    conv = [{"role": "user", "content": instruction}]

    chat_completion = client.chat.completions.create(
        model=llm_name,  # "gpt-3.5-turbo"
        messages=conv,
        stream=False,
        functions=api_doc_list
    )

    msg = chat_completion.choices[0].message
    msg = msg.model_dump()
    conv.append(msg)
    return conv 


def perform_task3(tool_name, api_name, instruction, llm_name="gpt-4-8k"):

    api_doc = convert_doc_to_openai_format(api_docs[tool_name][api_name]) 
    api_doc_list = [api_doc]

    conv = [{"role": "user", "content": instruction}]

    chat_completion = client.chat.completions.create(
        model=llm_name,  # "gpt-3.5-turbo"
        messages=conv,
        stream=False,
        functions=api_doc_list
    )

    msg = chat_completion.choices[0].message
    msg = msg.model_dump()
    conv.append(msg)
    return conv 


def perform_task4(tool_name, api_name, instruction, llm_name="gpt-4-8k"):

    api_doc = convert_doc_to_openai_format(api_docs[tool_name][api_name]) 
    api_doc_list = [api_doc]

    conv = [{"role": "user", "content": instruction}]
    tools = [{"type": "function", "function": api} for api in api_doc_list]
    chat_completion = client.chat.completions.create(
        model=llm_name,  # "gpt-3.5-turbo"
        messages=conv,
        stream=False,
        tools=tools
    )
    
    msg = chat_completion.choices[0].message
    msg_dict = msg.model_dump()
    conv.append(msg_dict)

    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        func_call = tool_call.function
        tool_ret = toolset.call_tool(tool_name, api_name, json.loads(func_call.arguments))
        tool_ret_str = str(tool_ret)
        tool_msg = {
            "role": "tool",
            "name": api_name,
            "content": tool_ret_str,
            "tool_call_id": tool_call.id
        }
        # print(message)
        conv.append(tool_msg)

        # second turn
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-4-8k",  # "gpt-3.5-turbo"
                messages=conv,
                stream=False
            )
            
            msg = chat_completion.choices[0].message
            msg_dict = msg.model_dump()
            conv.append(msg_dict)
        except Exception as e:
            return conv

    return conv 



def perform_task5(instruction, llm_name="gpt-4-8k"):

    conv = [{"role": "user", "content": instruction}]

    chat_completion = client.chat.completions.create(
        model=llm_name,  # "gpt-3.5-turbo"
        messages=conv,
        stream=False
    )

    msg = chat_completion.choices[0].message
    msg = msg.model_dump()  
    conv.append(msg)
    return conv 


def perform_task6(conv_history, llm_name="gpt-4-8k"):

    chat_completion = client.chat.completions.create(
        model=llm_name,  # "gpt-3.5-turbo"
        messages=conv_history,
        stream=False
    )
    
    msg = chat_completion.choices[0].message
    msg = msg.model_dump()  
    conv = conv_history + [msg]
    return conv 


def perform_task7(tool_name, api_name, instruction, dep_tools, llm_name="gpt-4-8k"):
    api_name_to_tool_name_map = {api_name: tool_name}

    api_doc = convert_doc_to_openai_format(api_docs[tool_name][api_name]) 
    api_doc_list = [api_doc]
    for dep_t, dep_api in dep_tools:
        api_doc = convert_doc_to_openai_format(api_docs[dep_t][dep_api]) 
        api_doc_list.append(api_doc)
        api_name_to_tool_name_map[dep_api] = dep_t

    conv = [{"role": "user", "content": instruction}]
    tools = [{"type": "function", "function": api} for api in api_doc_list]
    for _ in range(10):  # maximum 10 rounds

        chat_completion = client.chat.completions.create(
            model=llm_name,  # "gpt-3.5-turbo"
            messages=conv,
            stream=False,
            tools=tools,
            parallel_tool_calls = False
        )
        
        msg = chat_completion.choices[0].message
        msg_dict = msg.model_dump()
        conv.append(msg_dict)
        
        # print(msg_dict)
        if msg.tool_calls:
            # tool_call = msg.tool_calls[0]
            for tool_call in msg.tool_calls:
                func_call = tool_call.function
                if func_call.name not in api_name_to_tool_name_map:
                    raise Exception("invalid function name")
                tool_ret = toolset.call_tool(api_name_to_tool_name_map[func_call.name], func_call.name, json.loads(func_call.arguments))
                tool_ret_str = str(tool_ret)
                tool_msg = {
                    "role": "tool",
                    "name": func_call.name,
                    "content": tool_ret_str,
                    "tool_call_id": tool_call.id
                }
                conv.append(tool_msg)
                # print(tool_msg)
        else:
            break

    return conv 



def perform_task8(instruction, tools, llm_name="gpt-4-8k"):
    api_doc_list = []
    for tool, api in tools:
        api_doc = convert_doc_to_openai_format(api_docs[tool][api]) 
        api_doc_list.append(api_doc)
    
    api_doc_str_list = [f"{i+1}. " + json.dumps(api_doc, ensure_ascii=False).replace("\n", " ") for i, api_doc in enumerate(api_doc_list)]
    api_doc_text = "\n".join(api_doc_str_list)

    prompt = f"For a given problem, think how you can solve it with the help of provided tools.\n\nUser problem: {instruction}\n\nTools:\n" + api_doc_text

    conv = [{"role": "user", "content": prompt}]

    chat_completion = client.chat.completions.create(
        model=llm_name,  # "gpt-3.5-turbo"
        messages=conv,
        stream=False
    )

    msg = chat_completion.choices[0].message
    msg = msg.model_dump()  
    conv.append(msg)
    return conv 


