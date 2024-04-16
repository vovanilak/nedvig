from aiogram import BaseMiddleware
from aiogram.types import Message

from cachetools import TTLCache

class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self, time_limit = 0.5) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(self, handler, event: Message, data):
        if event.chat.id in self.limit:
            return
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data)