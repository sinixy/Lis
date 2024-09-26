from dotenv import load_dotenv
from os import getenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
HOST_ID = int(getenv('HOST_ID'))

LLM_API_KEY = getenv('LLM_API_KEY')
LLM_MODEL_ENDPOINT = getenv('LLM_MODEL_ENDPOINT')

DATA_DIR = getenv('DATA_DIR')