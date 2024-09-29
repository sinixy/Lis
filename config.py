from dotenv import load_dotenv
from os import getenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
HOST_ID = int(getenv('HOST_ID'))

MLAB_LLM_API_KEY = getenv('MLAB_LLM_API_KEY')
MISTRAL_LLM_API_KEY = getenv('MISTRAL_LLM_API_KEY')

DB_HOST = getenv('DB_HOST')
DB_NAME = getenv('DB_NAME')
DATA_DIR = getenv('DATA_DIR')