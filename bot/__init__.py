from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN, LLM_API_KEY, LLM_MODEL_ENDPOINT
from lis import Lis
from .middlewares import GlobalMiddleware


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.message.middleware(GlobalMiddleware())
dp.callback_query.middleware(GlobalMiddleware())

lis = Lis(LLM_MODEL_ENDPOINT, LLM_API_KEY)

@dp.message(CommandStart())
async def start(message: Message):
    return

@dp.message()
async def answer(message: Message):
    print('hey')
    if text := message.text:
        lis_response = await lis.send_message(text)
        await message.answer(lis_response)