import asyncio
import logging
import sys
import os
from os import getenv
from handlers import start, registration, arenda_buy, contin, sell, phone, error
from aiogram import Bot, Dispatcher
#from aiogram_sqlite_storage.sqlitestore import SQLStorage
from middlewares.antiflood import AntiFloodMiddleware
from db.create import create_table

if not os.path.exists('data/db.sqlite'):
    create_table()
    
#my_storage = SQLStorage('messages.db', serializing_method = 'pickle')
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()

async def main():
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(AntiFloodMiddleware())
    dp.include_routers(
        start.router,
        registration.router,
        contin.router,
        phone.router,
        arenda_buy.router,
        sell.router,
        error.router,
    )
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())