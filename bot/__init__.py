from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import types as aiotypes

from config import BOT_TOKEN, MISTRAL_LLM_API_KEY, MLAB_LLM_API_KEY
from character import Character
from agent import MistralAgent, MLabAgent
from models.dialog import Dialog
from utils import construct_lis_prompt
from .middlewares import GlobalMiddleware


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.message.middleware(GlobalMiddleware())
dp.callback_query.middleware(GlobalMiddleware())


class Conversation:

    MISTRAL_AGENT = MistralAgent(MISTRAL_LLM_API_KEY)
    MLAB_AGENT = MLabAgent(MLAB_LLM_API_KEY)

    def __init__(self):
        self.lis = Character(Conversation.MLAB_AGENT, construct_lis_prompt('lis.txt'))

        self.dialog: Dialog = None

    async def init(self):
        self.dialog = await Dialog.load_dialog()

    async def step(self, message: aiotypes.Message) -> str:
        self.dialog.prune()
        self.dialog.add(message.message_id, message.text, 'user')
        response, _ = await self.lis.get_response(
            [{'role': 'system', 'content': self.lis.bio}, *self.dialog.to_llm_list()]
        )
        if response[0] == '"' and response[-1] == '"': response = response[1:-1]
        return response

conversation = Conversation()

@dp.message(CommandStart())
async def start(message: aiotypes.Message):
    return

@dp.message()
async def answer(message: aiotypes.Message):
    if message.text:
        lis_response = await conversation.step(message)
        response = await message.answer(lis_response)
        conversation.dialog.add(response.message_id, response.text, 'assistant')