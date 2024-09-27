from dotenv import load_dotenv
from os import getenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
HOST_ID = int(getenv('HOST_ID'))

U_LLM_API_KEY = getenv('U_LLM_API_KEY')
M_LLM_API_KEY = getenv('M_LLM_API_KEY')
U_LLM_MODEL_ENDPOINT = getenv('U_LLM_MODEL_ENDPOINT')

DATA_DIR = getenv('DATA_DIR')