from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from db import info
import os
from aiogram import MagicFilter

class CheckRepeat(Filter):
    def __init__(self, stage):#переменные каторые будут использоваться в других методов
        self.stage=stage
    async def __call__ (self, message: Message, state: FSMContext):#действия после вызова класса.
        data = await state.get_data()#получение всего хранилища
        return self.stage in data.keys()#проверяет определенные ключи в хранилище(словарик).

"""
class CheckRepeat(Filter):
    def __init__(self, column_name):
        self.column_name = column_name
    async def __call__ (self, message: Message):
        if hasattr(message, 'chat'):
            data = await info.find_user_info(
                chat_id=message.chat.id,
                column_name=self.column_name,
            )
        else:
            data = await info.find_user_info(
                chat_id=message.message.chat.id,
                column_name=self.column_name,
            )
        return data

"""
class CheckAdmin(MagicFilter):
    async def __call__ (self, message: Message):
        ads = os.getenv('ADMIN').split(',')
        return message.chat.id in ads
        
        