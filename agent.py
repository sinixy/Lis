from mistralai import Mistral, ToolCall
import aiohttp


class Agent:

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def complete(self, messages: list[dict]):
        raise NotImplementedError


class MistralAgent(Agent):

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.model = Mistral(api_key)

    async def complete(self, messages: list[dict], tools: list[dict] = []) -> tuple[str, list[ToolCall]]:
        resp = await self.model.chat.complete_async(
            model='open-mistral-nemo', messages=messages,
            temperature=0.3, tools=[]
        )
        if resp:
            return resp.choices[0].message.content, resp.choices[0].message.tool_calls
        else:
            raise Exception('Failed to get Mistral response')
        

class MLabAgent(Agent):

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.endpoint = 'https://modelslab.com/api/v6/llm/uncensored_chat'
        self.session = aiohttp.ClientSession()

    async def complete(self, messages: list[dict], tools: list[dict] = []) -> tuple[str, list[ToolCall]]:
        async with self.session.post(
            self.endpoint,
            json={'key': self.api_key, 'messages': messages, 'max_tokens': 512}
        ) as response:
            resp = await response.json()
            if resp['status'] == 'success':
                return resp['message'], []
            else:
                raise Exception(resp['status'])