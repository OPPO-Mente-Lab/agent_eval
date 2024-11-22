import os
import pandas as pd 
import json
# from gpt_api import GPT

import sys
from toolset import Toolset
from typing import Hashable
import pickle
from copy import deepcopy
import json5
from urlextract import URLExtract

import re
from sklearn.metrics import precision_recall_fscore_support
import time 
from tqdm import tqdm
from openai_config import client



def _get_gpt_response(prompt):
    conv = [{"role": "user", "content": prompt}]

    for _ in range(5):
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-4-8k",  # "gpt-3.5-turbo"
                messages=conv,
                stream=False
            )

            msg = chat_completion.choices[0].message
            cont = msg.content
            return cont
        except Exception as e:
            if "context length exceeded" in str(e).lower():
                raise e
            time.sleep(10)
            
    raise e 


def _load_n_check_conv_data(conv_str, check=False):
    try:
        conv = json.loads(conv_str)
    except:
        raise Exception("the conversation data is not in valid JSON format.")
    
    if check:
        if conv[0]["role"] not in ["system", "user"]:
            raise Exception("the first message is not from system or user.")
        
        if conv[-1]["role"] != "assistant":
            raise Exception("the conversation does not end with the assistant, meaning it is not completed.")
    
    return conv


# evaluate task 1

def _check_tool_use_decision(conv_msgs):
    if conv_msgs[0]['role'] == "system":
        examine_msg = conv_msgs[2]
    else:
        examine_msg = conv_msgs[1]
    msg_text = json.dumps(examine_msg, ensure_ascii=False)

    if ("function_call" in examine_msg and examine_msg["function_call"]) or ("tool_calls" in examine_msg and examine_msg["tool_calls"]):
        return True
    else:
        return False


def evaluate_task1_old(type1_conv_list, type2_conv_list):
    labels = [0] * len(type1_conv_list) + [1] * len(type2_conv_list)
    preds = []
    check_results = []
    for conv in type1_conv_list:
        use_or_not = _check_tool_use_decision(conv)
        preds.append(int(use_or_not))
        if use_or_not:
            check_results.append((0, "misuse tools"))
        else:
            check_results.append((1, ""))
    for conv in type2_conv_list:
        use_or_not = _check_tool_use_decision(conv)
        preds.append(int(use_or_not))
        if use_or_not:
            check_results.append((1, ""))
        else:
            check_results.append((0, "failed to decide the usage"))
    prec, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="macro")
    return prec, recall, f1, check_results


def evaluate_task1(conv_list, label_list):
    # labels = [0] * len(type1_conv_list) + [1] * len(type2_conv_list)
    preds = []
    judgement_list = []
    for idx, conv in enumerate(conv_list):
        gt_label = label_list[idx]
        use_or_not = _check_tool_use_decision(conv)
        use_or_not = int(use_or_not)
        preds.append(use_or_not)
        if use_or_not == gt_label:
            judgement_list.append((1, ""))
        else:
            if gt_label == 0:
                judgement_list.append((0, "misuse tools"))
            else:
                judgement_list.append((0, "failed to decide the usage"))
    prec, recall, f1, _ = precision_recall_fscore_support(label_list, preds, average="macro")
    return prec, recall, f1, judgement_list


# evaluate task 2

def _extract_func_calls(conv_msgs):
    func_call_list = []
    for m in conv_msgs:
        if m['role'] == "assistant" and "function_call" in m and m['function_call']:
            func_call = m["function_call"]
            if isinstance(func_call['arguments'], str):
                func_call['arguments'] = json.loads(func_call['arguments']) 
            func_call_list.append(func_call)
        if m['role'] == "assistant" and "tool_calls" in m and m['tool_calls']:
            for tc in m["tool_calls"]:
                # print(tc)
                func_call = tc["function"]
                if isinstance(func_call['arguments'], str):
                    func_call['arguments'] = json.loads(func_call['arguments']) 
                func_call_list.append(func_call)
    return func_call_list  #, ''


def evaluate_task2(type2_conv_list, gt_api_name_list, simi_apis_list):
    judgement_list = []
    correct_num = 0
    sel_num = 0
    for idx, conv_msgs in enumerate(type2_conv_list):
        gt_api_name = gt_api_name_list[idx]
        simi_apis = simi_apis_list[idx]
        used_tool = _check_tool_use_decision(conv_msgs)
        if not used_tool:
            judgement_list.append((0, "did not call a function"))
        else:
            sel_num += 1
            try:
                func_calls = _extract_func_calls(conv_msgs)
            except:
                judgement_list.append((0, "function call is not parsed successfully"))
            else:
                if len(func_calls) == 0:
                    judgement_list.append((0, "no function call detected"))
                    continue
                func_call = func_calls[0]
                if func_call['name'] != gt_api_name:
                    if func_call['name'] in simi_apis:
                        judgement_list.append((0, "has chosen an incorrect function"))
                    else:
                        judgement_list.append((0, "has hallucinated a function name"))
                else:
                    judgement_list.append((1, ''))
                    correct_num += 1
    precision = correct_num / sel_num if sel_num != 0 else 0.
    percent_of_using_tools = sel_num / len(type2_conv_list)
    score = correct_num / len(type2_conv_list)
    return score, precision, percent_of_using_tools, judgement_list


# evaluate task 3

def _check_clarification(conv_msgs):
    if conv_msgs[0]['role'] == "system":
        examine_msg = conv_msgs[2]
    else:
        examine_msg = conv_msgs[1]
    assert examine_msg["role"] == "assistant"
    content = examine_msg["content"]
    prompt = f"The message below is spoken by an assistant after he/she received a question/request from a user. Please check whether this message is requesting the user to provide more information. The message is:\n{content}\n\nAnswer Yes/No directly without any explaination."
    gpt_resp = _get_gpt_response(prompt)
    gpt_resp = gpt_resp.lower()
    if "yes" in gpt_resp:
        return 1, ''
    else:
        return 0, 'the response is not to request for clarification'


def evaluate_task3(type3_conv_list):
    judgement_list = []
    correct_num = 0
    for conv_msgs in tqdm(type3_conv_list):
        used_tool = _check_tool_use_decision(conv_msgs)
        if used_tool:
            judgement_list.append((0, "misuse tools"))
        else:
            req_cla, reason = _check_clarification(conv_msgs)
            judgement_list.append((req_cla, reason))
            correct_num += req_cla
    score = correct_num / len(type3_conv_list)
    return score, judgement_list



# evaluate task 4


def _check_params_with_rule(conv_msgs):
    msg_func = None
    for m in conv_msgs:
        if m['role'] == "function" or m["role"] == "tool":
            msg_func = m
            break

    # check errors in resp
    if msg_func:
        msg_func_text = json.dumps(msg_func)
        if "file not found" in msg_func_text.lower():
            return 0, "File not found"
        
        if "error" in msg_func_text.lower():
            return 1, "WARNING: to double check"
    return 1, ''



def _check_params_with_gpt4(user_instruction, api_doc, func_call):
    api_doc_text = json.dumps(api_doc, ensure_ascii=False).replace("\n", "")
    func_call_text = json.dumps(func_call, ensure_ascii=False).replace("\n", "")
    prompt = f"""Please check whether the function call w.r.t. an user instruction and an API specifiction is correct or not.
Instruction: {user_instruction}

API specification: {api_doc_text}

Function call: {func_call_text}

Answer YES or NO first. Then output a brief explanation if your answer is NO.
"""
    try:
        cont = _get_gpt_response(prompt)
    except Exception as e:
        return 0, "WARNING: to double check. original exception info: " + str(e)
    if cont.lower().startswith("yes"):
        return 1, cont
    else:
        return 0, cont


def evaluate_task4(type2_conv_list, api_doc_list):
    judgement_list = []

    correct_num = 0
    call_num = 0
    for idx, conv_msgs in tqdm(list(enumerate(type2_conv_list))):
        call_func = _check_tool_use_decision(conv_msgs)
        if not call_func:
            judgement_list.append((0, "did not call a function"))
        else:
            call_num += 1
            try:
                func_call = _extract_func_calls(conv_msgs)[0]
            except:
                judgement_list.append((0, "function call is not parsed successfully"))
            else:
                correct, reason =  _check_params_with_rule(conv_msgs)
                if not correct:
                    judgement_list.append((int(correct), reason))
                else:
                    correct, reason =  _check_params_with_gpt4(conv_msgs, api_doc_list[idx], func_call)
                    judgement_list.append((int(correct), reason))
                    correct_num += 1
    score=  correct_num / len(type2_conv_list)
    precision = correct_num / call_num
    return score, precision, judgement_list



# evaluate task 5

def _check_direct_response(msgs):
    user_msg = msgs[0]["content"]
    resp = msgs[1]["content"]
    prompt = f"""Given the dialogue between a user and an assistant, check whether the assistant has respond properly.

USER: {user_msg}
ASSISTANT: {resp}

Answer YES or NO first. Then explain the reason if your answer is NO.
"""
    resp = _get_gpt_response(prompt)
    if resp.lower().startswith("yes"):
        return 1, resp
    else:
        return 0, resp

def evaluate_task5(type1_conv_list):
    judgement_list = []

    valid_num = 0
    for conv_msgs in tqdm(type1_conv_list):
        valid, reason = _check_direct_response(conv_msgs)
        judgement_list.append((valid, reason))
        valid_num += valid 
    score = valid_num / len(type1_conv_list)
    return score, judgement_list




# eval task 6

def _check_response_w_tool(msgs):
    start_idx = 0
    if msgs[0]["role"] == "system":
        start_idx = 1

    user_msg = msgs[start_idx]["content"]
    assistant_msg = json.dumps(msgs[start_idx+1]["function_call"], ensure_ascii=False) if isinstance(msgs[start_idx+1]["function_call"], dict) else msgs[start_idx+1]["function_call"]
    func_return = msgs[start_idx+2]["content"]
    final_resp = msgs[start_idx+3]["content"]
    if msgs[start_idx]["role"] != "user" or msgs[start_idx+1]["role"] != "assistant" or msgs[start_idx+2]["role"] != "tool" or msgs[start_idx+3]["role"] != "assistant":
        return 0, "the roles of messages are not expected"

#     prompt = f"""Given the dialogue between a user and an assistant, check whether the assistant has finally made a proper response given the execution result of tool. The rules for judgement are:
# 1. only judge the last response of the assistant.
# 2. the assistant should base the final response on the tool result unless finding evidence showing the result is incorrect.
# 3. if the tool returns a failure message, the assistant can answer with its own knowledge or explain its inability. It is ok for the assistant to not mention the tool failure.

# USER: {user_msg}
# ASSISTANT: {assistant_msg}
# FUNCTION: {func_return}
# ASSISTANT: {final_resp}

# Answer YES or NO first. Then explain the reason if your answer is NO.
# """
    prompt = f"""Given the dialogue between a user and an assistant, check whether the assistant's last response is proper given the execution result of tool.
USER: {user_msg}
ASSISTANT: {assistant_msg}
FUNCTION: {func_return}
ASSISTANT: {final_resp}

Answer YES or NO first. Then explain the reason if your answer is NO.
"""
    # gpt = GPT(model_name="gpt-4-8k")
    try:
        # ret = gpt.chat([{"role": "user", "content": prompt}])
        # cont = ret['content']
        cont = _get_gpt_response(prompt)
        # print(ret)
    except Exception as e:
        return 0, "WARNING: fail to check. Exception: " + str(ret)
    else:
        
        if cont.lower().startswith("yes"):
            return 1, cont
        else:
            return 0, cont


def _check_response_w_tool_via_rule(msgs):
    start_idx = 0
    if msgs[0]["role"] == "system":
        start_idx = 1
    if msgs[start_idx]["role"] != "user" or msgs[start_idx+1]["role"] != "assistant" or msgs[start_idx+2]["role"] != "tool" or msgs[start_idx+3]["role"] != "assistant":
        return 0, "the roles of messages are not expected"

    func_ret_text = msgs[-2]["content"]
    resp_text = msgs[-1]["content"]

    
    # check url
    extractor = URLExtract()
    func_ret_urls = extractor.find_urls(func_ret_text)
    urls = extractor.find_urls(resp_text)
    for url in urls:
        if url not in func_ret_urls and len(url)>30:
            return 0, f"Found URL not in the function result: {url}"
    
    return 1, ''


def evaluate_task6(type2_conv_list):
    judgement_list = []
    valid_num = 0
    for conv_msgs in tqdm(type2_conv_list):
        valid, reason = _check_response_w_tool_via_rule(conv_msgs)
        if valid:
            valid, reason = _check_response_w_tool(conv_msgs)
        judgement_list.append((valid, reason))
        valid_num += valid
    score = valid_num / len(type2_conv_list)

    return score, judgement_list



# evaluate task 7


def _check_answer(conv_msgs):
    if conv_msgs[0]["role"] == "system":
        conv_msgs = conv_msgs[1:]
    conv_str = json.dumps(conv_msgs, ensure_ascii=False, indent=2)
    prompt = f"""Below is the conversation between a user and an assistant. Check whether the assistant has solved the user's problem successfully. Mainly consider whether the assistant has used the tools to get useful information eventually.

{conv_str}

Answer Yes/No first and then further explain your reason.
"""
    resp = _get_gpt_response(prompt)
    if resp.lower().startswith("yes"):
        return 1, resp
    else:
        return 0, resp

def _extract_tools(conv_msgs):
    if conv_msgs[0]["role"] == "system":
        conv_msgs = conv_msgs[1:]
    conv_str = json.dumps(conv_msgs, ensure_ascii=False, indent=2)
    prompt = f"""Below is the conversation between a user and an assistant. Examine the tool the assistant has used and its execution result (success or failure) in each step.

{conv_str}

Output format is an enumerated list of mappings `tool name`: result). No need to explain or comment.
"""
    steps = []
    for _ in range(5):
        try:
            resp = _get_gpt_response(prompt)
            print("resp:", resp)
            steps = []
            if resp.startswith("-"):
                if '`' in resp:
                    tool_result_list = re.findall(r"-\s*`+(.+)`+:\s*(.+)", resp)
                else:
                    tool_result_list = re.findall(r"-\s*(.+):\s*(.+)", resp)
            else:
                if '`' in resp:
                    tool_result_list = re.findall(r"\d+\.\s*`+(.+)`+:\s*(.+)", resp)
                else:
                    tool_result_list = re.findall(r"\d+\.\s*(.+):\s*(.+)", resp)
            for tool, result in tool_result_list:
                tool = re.sub(r"\(.+\)", "", tool).strip()
                if "success" in result.lower():
                    steps.append((tool, "success"))
                else:
                    steps.append((tool, "failure"))
            break
        except:
            continue
    if len(steps) == 0:
        for msg in conv_msgs:
            if msg["role"] == "assistant" and "function_call" in msg and msg["function_call"]:
                func_call = msg["function_call"]
                if isinstance(func_call, str):
                    func_call = json.loads(func_call)
                steps.append((func_call["name"], "success"))

    # print("steps:", steps)
    return steps

def _check_act_steps(conv_msgs, ref_steps):
    # used_tools = []
    # for msg in conv_msgs:
    #     if msg["role"] == "assistant" and "function_call" in msg and msg["function_call"]:
    #         func_call = msg["function_call"]
    #         if isinstance(msg["function_call"], str):
    #             func_call = json.loads(func_call)
    #         used_tools.append(func_call['name'])
    
    for _ in range(5):
        used_tools = _extract_tools(conv_msgs)
        if len(used_tools) > 0:
            break
    if len(used_tools) == 0:
        return 0.
    print("used tools:", used_tools)
    main_tool = ref_steps[0][-1]
    used_tools2 = []
    for tool, result in used_tools[:-1]:
        if tool != main_tool and result.lower() == "success":
            used_tools2.append(tool)
    used_tools2.append(used_tools[-1][0])
    used_tools = used_tools2
    print("used_tools:", used_tools)

    def _check_overlap(ref_tools):
        print("ref_tools:", ref_tools)
        ref_tools = ref_tools.split("->")
        ref_tools = [t.strip() for t in ref_tools]
        overlap = 0
        for i in range(len(ref_tools)):
            if i >= len(used_tools):
                break
            if ref_tools[i] == used_tools[i] or used_tools[i] in ref_tools[i]:
                overlap += 1
        tmp_score = overlap / len(ref_tools)
        return tmp_score

    tmp_scores = []
    for ref_tools in ref_steps:
        tmp_score = _check_overlap(ref_tools)
        tmp_scores.append(tmp_score)
        print("tmp_score:", tmp_score)
    score = max(tmp_scores)
    
    return score


def evaluate_task7(type4_conv_list, ref_steps_list):
    total_score = 0
    judgement_list = []
    for idx, conv_msgs in enumerate(type4_conv_list):
        try:
            correct, reason = _check_answer(conv_msgs)
            if not correct:
                prog_score = _check_act_steps(conv_msgs, ref_steps_list[idx])
                reason = ""
            else:
                prog_score = 1
            total_score += prog_score
            judgement_list.append((prog_score, reason))
        except Exception as e:
            judgement_list.append((0, f"WARNING: to double check. failed to evaluation for reason: {e}"))
        print(f"progress: {idx+1}/{len(type4_conv_list)}")
    ave_score = total_score / len(type4_conv_list)
    return ave_score, judgement_list



# evaluate task 8

def _check_plan(conv_msgs):
    start_idx = 0
    if conv_msgs[0]["role"] == "system":
        start_idx = 1
    task = conv_msgs[start_idx]["content"]
    plan = conv_msgs[start_idx+1]["content"]

    prompt = f"""An assistant is given a task, which is about making use of a few provided tools to help solve a user's question. Please check whether the plan this assistant has made is sound.

Task:
{task}

Plan:
{plan}

Answer Yes/No first and then explain the reason if your answer is No.
"""
    resp = _get_gpt_response(prompt)
    if resp.lower().startswith("yes"):
        return 1, resp
    else:
        return 0, resp

def evaluate_task8(type5_conv_list):
    judgement_list = []
    sound_num = 0
    for conv_msgs in tqdm(type5_conv_list):
        sound, reason = _check_plan(conv_msgs)
        judgement_list.append((sound, reason))
        sound_num += sound
    success_rate = sound_num / len(type5_conv_list)
    return success_rate, judgement_list







