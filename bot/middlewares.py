from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable, Union

from config import HOST_ID


class GlobalMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[types.Message, types.CallbackQuery],
        data: Dict[str, Any]
    ):
        if event.from_user.id == HOST_ID:
            return await handler(event, data)