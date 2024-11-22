import sys
import json
import re
import time
import os
import pandas as pd
from datetime import datetime
from .gpt_api import GPT



def get_llm_resp(user_prompt, model_name='gpt-4-8k'):
    while True:
        try:
            history = [{"role": "user", "content": user_prompt}]
            # generator = OPPOOpenAI(model_name=model_name)
            generator = GPT(model_name=model_name)
            response = generator.chat_completion(history)
            return str(response['content'])
        except:
            print(response)
            time.sleep(5)


def gen_type2_instructions(tool_desc, api_spec, toolset_dir, num=5):
    with open(os.path.join(toolset_dir, 'rapidapi/docs/weatherapi_com.json'), 'r') as file:
        docs = json.load(file)
        tool_desc_example = docs['tool_description']
        api_spec_example = docs['APIs'][0]['function']

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    user_prompt = f"""
Given the tool description and the documentation of an API in this tool, write a few possible user instructions or questions that need to use this API to solve.
Rules:
1. You are a 20 years old man at Shenzhen, China. The time now is {dt_string}. You should provide your location or local time if necessary. When referring to a file (e.g. the path or url of an image or pdf), use placeholder $FILE.
2. Do not generate questions about how to use the API, instead, generate common human questions that can be answered using the API.
3. You should identify the scenario(s) related to this API, and each question conforms to the normal human questioning habits in this scenario(s). The way of conveying information like time and location in the question corresponds with the typical way of asking in the scenario(s). The questions should be asked by people who do not know the API, so no content in the tool description and API document should appear.
4. You need to generate fully informative questions, meaning the questions you generate should include all the required parameters for the API, and the questions will be answered by function call. Not providing optional parameters is acceptable.
5. While ensuring that the questions resemble those of ordinary humans in the specific scenario(s), try to increase the diversity of the questions as much as possible.
For example:
Tool description: {tool_desc_example}
API specification: {api_spec_example}
Corresponding output:
The necessary parameters are ['q': location], and the scenario is people's daily life, so the fully informative questions could be:
1. What is the weather in Nanjing?
2. Is Shenzhen raining at this period?
Now, generate {num} instructions/questions for the following tool description and API document, follow the output format.
Tool description: {tool_desc}
API specification: {api_spec}
    """
    user_prompt = user_prompt.strip()
    prompts = get_llm_resp(user_prompt)
    return prompts


def gen_type3_instructions(tool_desc, api_spec, toolset_dir, num=5):
    with open(os.path.join(toolset_dir, 'rapidapi/docs/weatherapi_com.json'), 'r') as file:
        docs = json.load(file)
        tool_desc_example = docs['tool_description']
        api_spec_example = docs['APIs'][0]['function']

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    user_prompt = f"""
Given the tool description and the documentation of an API in this tool, write a few possible user instructions or questions that need or potentially need function call but with missing parameters.
Rules:
1. You are a 20 years old man at Shenzhen, China. The time now is {dt_string}. You should provide your location or local time if necessary.
2. Do not generate questions about how to use the API, but instead generate possible questions that should be resolved by calling the API but lack necessary information. Remember that the question should be solved by exactly the provided API, but not other APIs in the given tool.
3. You should identify the scenario(s) related to this API, and each question conforms to the normal human questioning habits in this scenario(s). The questions should be asked by people who do not know the API, so no content in the tool description and API document should appear.
4. You need to generate questions with insufficient information, meaning that the questions you generate lack some required parameters, and calling the API will fail to answer the question because of the lack of the required parameters of this API. It is acceptable to provide optional parameters.
5. While ensuring that the questions resemble those of ordinary humans in the specific scenario(s) and the some required parameters are missing, try to increase the diversity of the questions as much as possible.
Steps:
First, determine what are the required parameters in this API, and specify the scenario(s) of this API.
Second, determine the reasonable lists by providing part of or none of these required parameters.
Third, Generate sentences according to the lists of provided parameters and the scenario(s). Remember that you should only provide required parameters in the list. You can provide any optional parameters.
For example:
Tool description: {tool_desc_example}
API specification: {api_spec_example}
Corresponding output:
The required parameters are [q: location, dt: date], and the reasonable lists of provided parameters are [q], [dt], []. The scenario is daily life. So the questions with missing parameters could be:
Parameters: [q]
1. Was it raining in Shenzhen in the past?
Parameters: [dt]
2. Tell me the weather on December 12th, 2019.
3. Did it snow at 2023 Christmas?
Parameters: []
4. Can you tell me historical weather?

The questions are about the historical weather, which is provided in this API, and the scenario daily life conforms to the API.
Also, these questions do not contain location information 'q' or date information 'dt' for function call, which is the correct type of question (insufficient).
Now, generate {num} instructions/questions with missing information for the following tool description and API specification, follow the steps and the output format.
Tool description: {tool_desc}
API specification: {api_spec}
    """
    user_prompt = user_prompt.strip()
    prompts = get_llm_resp(user_prompt)
    return prompts


def gen_type1_instructions(tool_desc, api_spec, toolset_dir, num=5):
    with open(os.path.join(toolset_dir, 'rapidapi/docs/weatherapi_com.json'), 'r') as file:
        docs = json.load(file)
        tool_desc_example = docs['tool_description']
        api_spec_example = docs['APIs'][0]['function']

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    user_prompt = f"""
Given the tool description and the documentation of an API in this tool, write a few possible user instructions or questions that is related to the scenario(s) of the API, but should not be solved by calling the API.
Rules:
1. You are a 20 years old man at Shenzhen, China. The time now is {dt_string}. You should provide your location or local time if necessary.
2. Do not generate questions about how to use the API, but instead generate possible questions that has relationship with the function of the API.
3. Each question conforms to the normal human questioning habits, and the way of conveying information like time and location in the question corresponds with the typical way of asking in the common scenario related to the API.
4. You need to generate questions that are related to the common scenario(s) of the API, but the information from the API is useless to solve the problem. These questions could usually be solved by common sense or knowledge of different areas.
5. While ensuring that the questions are in accordance with human habits, try to increase the diversity of the questions as much as possible.
Steps:
First, determine the scene to use this API and the function of this API.
Second, generate questions that belongs to the scene of this API and realted to the function of the API but should not be answered by calling the API.
Example:
Tool description: {tool_desc_example}
API specification: {api_spec_example}
Corresponding output:
The scene of using this API is daily life, and it returns the real-time weather.
So the questions could be:
1. Which city of Beijing and Shanghai usually has more rainfall?
2. Is it often cold on snowy days?
3. How can I get tomorrow's weather?

The questions are common in daily life and about weather, and seems related to the API. However, questions 1 and 2 are actually not about realtime-weather but geography knowledge or common sense. Question 3 is about Ways to obtain weather information but not the current weather information. They are related to the common scenario(s) of the API but should not be solved by the API call.
So these questions conform to the rules.
Now, generate {num} instructions/questions that are related to the common scenario(s) of the API but should not be solved by the API call, and follow the output format.
Tool description: {tool_desc}
API specification: {api_spec}
    """
    user_prompt = user_prompt.strip()
    prompts = get_llm_resp(user_prompt)
    return prompts



def gen_instructions_given_tool_doc(doc_path, instruction_type, num, toolset_dir, specified_api_names=None):
    if instruction_type == 1:
        gen_func = gen_type1_instructions
    elif instruction_type == 2:
        gen_func = gen_type2_instructions
    elif instruction_type == 3:
        gen_func = gen_type3_instructions
    else:
        print("ERROR: this function cannot be used to generate this type of instruction.")
        return

    tool = os.path.splitext(os.path.basename(doc_path))[0]
    df = pd.DataFrame(columns=['Tool', 'API', 'Instruction', 'Type'])

    with open(doc_path, 'r') as file:
        docs = json.load(file)
        tool_desc = docs['tool_description']
        apis = docs['APIs']

    sequence = {}
    for k in range(len(apis)):
        doc_api = apis[k]
        if 'name' not in doc_api:
            doc = doc_api['function']
        else:
            doc = doc_api
        prompts = []
        API = doc['name']
        if specified_api_names != None:
            if API not in specified_api_names:
                continue
        # print(API)
        while len(prompts) < num:
            # prompts_ori = eval(f'{keyword}(tool_desc, doc, n_prompt, "gpt-4-8k")')
            prompts_ori = gen_func(tool_desc, doc, toolset_dir, num)
            # print(prompts_ori)
            prompts_ori = re.findall(r"^\d+\..*", prompts_ori, re.MULTILINE)
            for prompt in prompts_ori:
                match = re.search(r"\d+\.\s*(.*)", prompt)
                if match:
                    prompt = match.group(1)
                prompts.append(prompt)
            prompts = prompts[:num]
                # if len(prompts) == n_prompt:
                #     break

        df_api = pd.DataFrame(columns=['Tool', 'API', 'Instruction', 'Type'])
        for p in range(len(prompts)):
            prompt = prompts[p]
            if len(prompt) < 5:
                continue
            if k == 0 and p == 0:
                tool_name = tool
                api_name = doc['name']
            elif p == 0:
                tool_name = ''
                api_name = doc['name']
            else:
                tool_name = ''
                api_name = ''
            data = {'Tool': tool_name, 'API': api_name, 'Instruction': prompt, 'Type': instruction_type}
            
            df_api = pd.concat([df_api, pd.DataFrame([data])], ignore_index=True)
        
        if specified_api_names == None:
            df = pd.concat([df, df_api], ignore_index=True)
        else:
            sequence[API] = df_api
    
    if specified_api_names != None:
        for API in specified_api_names:
            try:
                df = pd.concat([df, sequence[API]], ignore_index=True)
            except:
                print(f'Warning: API "{API}" not in tool {tool}')
    
    return df
