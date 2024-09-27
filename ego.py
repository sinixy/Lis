from mistralai import Mistral
import json

from models.dialog import Dialog
from utils import read_file


class Ego:

    def __init__(self, api_key: str, data_dir: str):
        self.api_key = api_key
        self.model = Mistral(api_key)

        self.data_dir = data_dir
        self.prompt = self.__construct_prompt()

    async def analyze(self, dialog: Dialog) -> str:
        messages = self.__get_messages(dialog)
        resp = await self.model.chat.complete_async(
            model='open-mistral-nemo', messages=messages,
            temperature=0.2
        )
        
        if resp:
            return resp.choices[0].message.content
        else:
            raise Exception('Failed to get Ego response')
            
    def __get_messages(self, dialog: Dialog):
        return [
            {'role': 'system', 'content': self.prompt},
            {'role': 'user', 'content': dialog.to_text('Host', 'Lis')}
        ]
    
    def __construct_prompt(self) -> str:
        template = read_file(f'{self.data_dir}/ego.txt')
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
