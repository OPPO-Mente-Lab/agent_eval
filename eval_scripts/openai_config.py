
from openai import OpenAI
import os


# set base url and key for openai or other llm services supporting assessement with openai client (e.g. ollama)
API_KEY = ""
BASE_URL = ""

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)



