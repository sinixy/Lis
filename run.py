import asyncio
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

async def run():
    from bot import bot, dp
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())