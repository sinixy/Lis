import aiohttp
import json

from config import LLM_API_KEY, LLM_MODEL_ENDPOINT, LIS_PROMPT
from models.dialog import Dialog


class Lis:

    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self.session = aiohttp.ClientSession()
        self.dialog = Dialog()

    async def send_message(self, message: str) -> str:
        self.dialog.prune()
        self.dialog.add(message, 'user')
        data = self.__get_request_data()
        async with self.session.post(self.endpoint, json=data) as response:
            resp = await response.json()
            if resp['status'] == 'success':
                print(json.dumps(resp['meta']['messages'], indent=2))
                lis_response = resp['message']
                self.dialog.add(lis_response, 'assistant')
                return lis_response
            else:
                self.dialog.pop()
                raise Exception(resp['status'])
            
    def __get_request_data(self):
        return {
            'key': self.api_key,
            'messages': [
                {'role': 'system', 'content': LIS_PROMPT},
                *self.dialog.to_list()
            ],
            'max_tokens': 1000
        }