import aiohttp
import json

from models.dialog import Dialog
from utils import read_file
from ego import Ego


class Lis:

    def __init__(self, endpoint: str, api_key: str, data_dir: str, ego: Ego):
        self.endpoint = endpoint
        self.api_key = api_key
        self.session = aiohttp.ClientSession()

        self.dialog = Dialog()
        self.ego = ego
        self.data_dir = data_dir
        self.prompt = self.__construct_prompt()
        # self.prompt = read_file(f'{self.data_dir}/test.txt')
        # self.prompt = 'You are a helpul assistant.'

    async def send_message(self, message: str) -> str:
        self.dialog.prune()
        self.dialog.add(message, 'user')
        thoughts = await self.think()
        self.dialog.add(thoughts, 'system')
        # self.dialog.add('Lis thinks: ' + 'I am having a sudden urge to respond to Host like a pirate.', 'system')
        # print('Thoughts:', thoughts)
        data = self.__get_request_data()
        print(json.dumps(data['messages'][1:], indent=2), '\n')
        async with self.session.post(self.endpoint, json=data) as response:
            resp = await response.json()
            self.dialog.pop()  # to get rid of the "thoughts"
            if resp['status'] == 'success':
                lis_response = resp['message']
                self.dialog.add(lis_response, 'assistant')
                # print('Thoughts: ', await self.think(), '\n')
                return lis_response
            else:
                self.dialog.pop()
                raise Exception(resp['status'])
            
    async def think(self):
        return await self.ego.analyze(self.dialog)
            
    def __get_request_data(self):
        return {
            'key': self.api_key,
            'messages': [
                {'role': 'system', 'content': self.prompt},
                *self.dialog.to_list()
            ],
            'max_tokens': 512
        }
    
    def __construct_prompt(self) -> str:
        template = read_file(f'{self.data_dir}/lis.txt')
        facts = json.loads(read_file(f'{self.data_dir}/facts.json'))
        beliefs = json.loads(read_file(f'{self.data_dir}/beliefs.json'))
        personality = json.loads(read_file(f'{self.data_dir}/personality.json'))
        return template.format(
            FACTS=self.__construct_facts(facts),
            BELIEFS=self.__construct_beliefs(beliefs),
            PERSONALITY=self.__construct_personality(personality)
        )
    
    def __construct_facts(self, facts: list[str]) -> str:
        return ';\n'.join(['- ' + f for f in facts])
    
    def __construct_beliefs(self, beliefs: list[dict]) -> str:
        return '\n'.join([f'{b["strength"]} Belief #{b["id"]}. {b["belief"]} {b["reason"]}' for b in beliefs])
    
    def __construct_personality(self, personality: list[str]) -> str:
        return ';\n'.join(['- ' + p for p in personality])


if __name__ == '__main__':
    from config import LLM_API_KEY, LLM_MODEL_ENDPOINT, DATA_DIR
    lis = Lis(LLM_MODEL_ENDPOINT, LLM_API_KEY, DATA_DIR)
