
# An Evaluation Mechanism of LLM-based Agents on Manipulating APIs

This repo contains codes and data for the paper "An Evaluation Mechanism of LLM-based Agents on Manipulating APIs", which has been accepted to EMNLP 2024 Findings.
In this work, we release one evaluation kit, consisting of (1) one set of tools, (2) data of 8 evaluation tasks examining different aspects of tool use capability, (3) automatic scoring scripts of 8 evaluation tasks.

## Structure of Files

* `data/`: instruction data, files (mainly images) for calling tools, and evaluation data for each task.
* `toolset/`: executable tools along with their corresponding documentation.
* `eval_scripts/`: codes for LLMs like GPT4 to performe tasks, automatic scoring.
* `reproduce/`: codes for assisting reproducing this work, e.g. prompts for generating initial instructions, search similar tools, produce data for tasks from instructions, etc.


## Install Python Environment

Python 3.9 with packages in requirements.txt.

## Usage of Toolset

Most tools are implemented by wrapping APIs deployed on RapidAPI, while a few are implemented by us.
These tools have a unified interface of calling functionalities and accessing  documentation.

To use this toolset, you need to get one `X-RapidAPI-Key` by registering [RapidAPI](https://rapidapi.com/hub).
Then, set your `X-RapidAPI-Key` in `toolset/config.yml`.
Afterwards, subscribe the following APIs on RapidAPI. All of them have free plan which is good to start with. 
  - [weatherapi_com](https://rapidapi.com/weatherapi/api/weatherapi-com/)
  - [news_api](https://rapidapi.com/bonaipowered/api/news-api14)
  - [public_holiday](https://rapidapi.com/theapiguy/api/public-holiday/)
  - [recipe_by_api_ninjas](https://rapidapi.com/apininjas/api/recipe-by-api-ninjas)
  - [objects_detection](https://rapidapi.com/ai-engine-ai-engine-default/api/objects-detection/)
  - [ocr_extract_text](https://rapidapi.com/iq.faceok/api/ocr-extract-text)
  - [web_capture](https://rapidapi.com/abdheshnayak/api/web-capture2)
  - [onecompiler_apis](https://rapidapi.com/onecompiler-onecompiler-default/api/onecompiler-apis)
  - [bing](https://rapidapi.com/Glavier/api/bing23)
  - [bing_search_apis](https://rapidapi.com/quangphatc3/api/bing-search-apis/)
  - [google_api](https://rapidapi.com/rphrp1985/api/google-api31)
  - [skyscanner80](https://rapidapi.com/datastore/api/skyscanner80)
  - [currency_exchange](https://rapidapi.com/fyhao/api/currency-exchange/)
  - [geocoding_by_api_ninjas](https://rapidapi.com/apininjas/api/geocoding-by-api-ninjas)
  - [airports](https://rapidapi.com/epsi/api/airports15/)
  - [list_of_all_countries_and_languages_with_their_codes](https://rapidapi.com/contactteamrkg/api/list-of-all-countries-and-languages-with-their-codes)
  - [tourist_attraction](https://rapidapi.com/ptwebsolution/api/tourist-attraction/)
  - [world_time_by_api_ninjas](https://rapidapi.com/apininjas/api/world-time-by-api-ninjas/)
  - [google_translate](https://rapidapi.com/googlecloud/api/google-translate1/)
  - [ip_geo_location](https://rapidapi.com/natkapral/api/ip-geo-location/)


## Config OpenAI key for running evaluation

Config the assessment to LLM like OpenAI GPTs in `eval_scripts/openai_config.py`.


## Producing more data, e.g. for new APIs

In the paper, the procedure of dataset construction is detailed in Appendix C, iillustrated with Fig.6 and 7.

We also provide some codes under `reproduce/` and data under `data/instructions/` for helping understand this process. Some notes are as below:

1. Generate initial instructions for each API.
`reproduce/generate_instruction*.ipynb` => `data/instructions/type-i,ii,iii,iv,v`.

2. Merge instructions of APIs.
 => `merged_instructions*.csv`.

3. Check the instruction data by human annotator.
=> `humancheck_instructions*.csv/xlsx`

4. Further process the instruction data and get the final instructions.
=> `process_instructions.ipynb`

5. After the instruction data are ready, produce data for each evaluation task.
`produce_data_for_task*.ipynb`









