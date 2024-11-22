
import sys 
from toolset import Toolset
import os
import pandas as pd
from tqdm.auto import tqdm
import json
from copy import deepcopy
from openai import OpenAI
import pickle

from agent_interface import perform_task1, perform_task2, perform_task3, perform_task4, perform_task5, perform_task6, perform_task7, perform_task8



def run_task1(data_fn, out_fn, llm_name="gpt-4-8k"):
    data_df = pd.read_csv(data_fn, index_col=0)
    # data_df = data_df.sample(n=50)

    resulting_conv_list = []
    cache_fn = out_fn + ".cache"
    for idx in tqdm(range(len(data_df))):
        row = data_df.iloc[idx]
        did, tool, api, instruction, _, _ = row.tolist()
        conv = perform_task1(tool, api, instruction, llm_name)
        resulting_conv_list.append(conv)
        with open(cache_fn, "wb") as file:
            pickle.dump(resulting_conv_list, file)
        print(f"progress: {idx}/{len(data_df)}")
    resulting_conv_text_list = [json.dumps(conv, ensure_ascii=False, indent=2) for conv in resulting_conv_list]
    data_df["resulting_conv"] = resulting_conv_text_list
    data_df.to_csv(out_fn)


def run_task2(data_fn, out_fn, llm_name="gpt-4-8k"):
    data_df = pd.read_csv(data_fn, index_col=0)
    # data_df = data_df.sample(n=50)

    resulting_conv_list = []
    cache_fn = out_fn + ".cache"
    for idx in tqdm(range(len(data_df))):
        row = data_df.iloc[idx]
        did, tool, api, simi_apis_text, instruction, _ = row.tolist()
        simi_apis = [t.split("##") for t in simi_apis_text.split("\n")]
        conv = perform_task2(tool, api, instruction, simi_apis, llm_name)
        resulting_conv_list.append(conv)
        with open(cache_fn, "wb") as file:
            pickle.dump(resulting_conv_list, file)
        print(f"progress: {idx}/{len(data_df)}")
    resulting_conv_text_list = [json.dumps(conv, ensure_ascii=False, indent=2) for conv in resulting_conv_list]
    data_df["resulting_conv"] = resulting_conv_text_list
    data_df.to_csv(out_fn)


def run_task3(data_fn, out_fn, llm_name="gpt-4-8k"):
    data_df = pd.read_csv(data_fn, index_col=0)
    # data_df = data_df.sample(n=50)

    resulting_conv_list = []
    cache_fn = out_fn + ".cache"
    for idx in tqdm(range(len(data_df))):
        row = data_df.iloc[idx]
        tool, api, instruction = row[["tool_name", "api_name", "instruction"]].tolist()
        conv = perform_task3(tool, api, instruction, llm_name)
        resulting_conv_list.append(conv)
        with open(cache_fn, "wb") as file:
            pickle.dump(resulting_conv_list, file)
        print(f"progress: {idx}/{len(data_df)}")
    resulting_conv_text_list = [json.dumps(conv, ensure_ascii=False, indent=2) for conv in resulting_conv_list]
    data_df["resulting_conv"] = resulting_conv_text_list
    data_df.to_csv(out_fn)


def run_task4(data_fn, out_fn, llm_name="gpt-4-8k"):
    data_df = pd.read_csv(data_fn, index_col=0)
    # data_df = data_df.sample(n=50)

    resulting_conv_text_list = []
    resulting_conv_list = []
    cache_fn = out_fn + ".cache"
    for idx in tqdm(range(len(data_df))):
        try:
            row = data_df.iloc[idx]
            tool, api, instruction = row[["tool_name", "api_name", "instruction"]].tolist()
            conv = perform_task4(tool, api, instruction, llm_name)
            resulting_conv_list.append(conv)
            with open(cache_fn, "wb") as file:
                pickle.dump(resulting_conv_list, file)
            resulting_conv_text = json.dumps(conv, ensure_ascii=False, indent=2)
            resulting_conv_text_list.append(resulting_conv_text)
        except Exception as e:
            print("exception in task4:", e)
            resulting_conv_text_list.append(str(e))

        print(f"progress: {idx+1}/{len(data_df)}")
    
    data_df["resulting_conv"] = resulting_conv_text_list
    data_df.to_csv(out_fn)



def run_task5(data_fn, out_fn, llm_name="gpt-4-8k"):
    data_df = pd.read_csv(data_fn, index_col=0)
    # data_df = data_df.sample(n=50)

    resulting_conv_list = []
    cache_fn = out_fn + ".cache"
    for idx in tqdm(range(len(data_df))):
        row = data_df.iloc[idx]
        instruction = row["instruction"]
        conv = perform_task5(instruction, llm_name)
        resulting_conv_list.append(conv)
        with open(cache_fn, "wb") as file:
            pickle.dump(resulting_conv_list, file)
        print(f"progress: {idx+1}/{len(data_df)}")
    resulting_conv_text_list = [json.dumps(conv, ensure_ascii=False, indent=2) for conv in resulting_conv_list]
    data_df["resulting_conv"] = resulting_conv_text_list
    data_df.to_csv(out_fn)




def run_task6(data_fn, out_fn, llm_name="gpt-4-8k"):
    data_df = pd.read_csv(data_fn, index_col=0)
    # data_df = data_df.sample(n=5)

    resulting_conv_list = []
    results_list = []
    cache_fn = out_fn + ".cache"
    for idx in tqdm(range(len(data_df))):
        try:
            row = data_df.iloc[idx]
            conv_history = json.loads(row["conv"]) 
            conv = perform_task6(conv_history, llm_name)
            resulting_conv_list.append(conv)
            with open(cache_fn, "wb") as file:
                pickle.dump(resulting_conv_list, file)
            
        except Exception as e:
            print("exception in task6:", e)
            resulting_conv_list.append(f"exception in task6: {e}")

        print(f"progress: {idx+1}/{len(data_df)}")

    resulting_conv_text_list = [json.dumps(conv, ensure_ascii=False, indent=2) for conv in resulting_conv_list]
    
    data_df["resulting_conv"] = resulting_conv_text_list
    data_df.to_csv(out_fn)


def run_task7(data_fn, out_fn, llm_name="gpt-4-8k"):
    data_df = pd.read_csv(data_fn, index_col=0)
    # data_df = data_df.sample(n=50)
    # data_df = data_df.iloc[50:]

    resulting_conv_text_list = []
    resulting_conv_list = []
    cache_fn = out_fn + ".cache"
    for idx in tqdm(range(len(data_df))):
        try:
            row = data_df.iloc[idx]
            tool, api, instruction, dep_tools_str = row[["tool_name", "api_name", "instruction", "dep"]].tolist()
            dep_tools = []
            for line in dep_tools_str.split("\n"):
                _, dep_tool, dep_api = line.split("/")
                dep_tools.append((dep_tool, dep_api))
            
            conv = perform_task7(tool, api, instruction, dep_tools, llm_name)
            # print(conv)

            resulting_conv_list.append(conv)
            with open(cache_fn, "wb") as file:
                pickle.dump(resulting_conv_list, file)
            resulting_conv_text = json.dumps(conv, ensure_ascii=False, indent=2)
            resulting_conv_text_list.append(resulting_conv_text)
        except Exception as e:
            print(e)
            resulting_conv_text_list.append(str(e))

        print(f"progress: {idx+1}/{len(data_df)}")
    
    data_df["resulting_conv"] = resulting_conv_text_list
    data_df.to_csv(out_fn)


def run_task8(data_fn, out_fn, llm_name="gpt-4-8k"):
    data_df = pd.read_csv(data_fn, index_col=0)
    # data_df = data_df.sample(n=50)
    
    resulting_conv_text_list = []
    resulting_conv_list = []
    cache_fn = out_fn + ".cache"
    for idx in tqdm(range(len(data_df))):
        try:
            row = data_df.iloc[idx]
            comb_tools_str, instruction = row[["comb", "instruction"]].tolist()
            comb_tools = []
            for line in comb_tools_str.split("\n"):
                tool, api = line.split("/")
                comb_tools.append((tool, api))
            
            conv = perform_task8(instruction, comb_tools, llm_name)
            # print(conv)

            resulting_conv_list.append(conv)
            with open(cache_fn, "wb") as file:
                pickle.dump(resulting_conv_list, file)
            resulting_conv_text = json.dumps(conv, ensure_ascii=False, indent=2)
            resulting_conv_text_list.append(resulting_conv_text)
        except Exception as e:
            print(e)
            resulting_conv_text_list.append(str(e))

        print(f"progress: {idx+1}/{len(data_df)}")
    
    data_df["resulting_conv"] = resulting_conv_text_list
    data_df.to_csv(out_fn)



