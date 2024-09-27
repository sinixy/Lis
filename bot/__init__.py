from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN, U_LLM_API_KEY, M_LLM_API_KEY, U_LLM_MODEL_ENDPOINT, DATA_DIR
from lis import Lis
from ego import Ego
from .middlewares import GlobalMiddleware


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.message.middleware(GlobalMiddleware())
dp.callback_query.middleware(GlobalMiddleware())

ego = Ego(M_LLM_API_KEY, DATA_DIR)
lis = Lis(U_LLM_MODEL_ENDPOINT, U_LLM_API_KEY, DATA_DIR, ego)

@dp.message(CommandStart())
async def start(message: Message):
    return

@dp.message()
async def answer(message: Message):
    if text := message.text:
        lis_response = await lis.send_message(text)
        await message.answer(lis_response)