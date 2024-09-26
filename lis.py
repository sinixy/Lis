from mistralai import Mistral
import json

from models.dialog import Dialog
from utils import read_file


class Lis:

    def __init__(self, api_key: str, data_dir: str):
        self.api_key = api_key
        self.model = Mistral(api_key)

        self.dialog = Dialog()
        self.data_dir = data_dir
        # self.prompt = self.__construct_prompt()
        self.prompt = read_file(f'{self.data_dir}/test.txt')
        # self.prompt = 'You are a helpul assistant.'

    async def send_message(self, message: str) -> str:
        self.dialog.prune()
        self.dialog.add(message, 'user')
        messages = self.__get_messages()
        resp = await self.model.chat.complete_async(
            model='open-mistral-nemo', messages=messages,
            temperature=0.4
        )
        
        if resp:
            lis_response = resp.choices[0].message.content
            self.dialog.add(lis_response, 'assistant')
            print(messages[1:])
            return lis_response
        else:
            self.dialog.pop()
            raise Exception('Failed to get Lis response')
            
    def __get_messages(self):
        return [
            {'role': 'system', 'content': self.prompt},
            *self.dialog.to_list()
        ]
    
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
