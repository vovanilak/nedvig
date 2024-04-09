from aiogram.types import Message
from filters.repeat import CheckReapeat
from aiogram import Router
from keyboard.builders import inline_kb
from aiogram import Bot, Dispatcher, filters, Router, F
from aiogram.filters import StateFilter
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.fsm.state import default_state
from data.book import nedvig
import os




router=Router()
router.message.filter(CheckReapeat("is_sell"))
@router.message()
async def router_y(message: Message, state: FSMContext):
    await message.answer("Ваши данные уже сохранены,вы уверены что хотите перезаписать эти данные?", reply_markup=inline_kb(["Да","Нет"]))
@router.callback_query(F.data.in_(["Да","Нет"]))
async def router_y_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data=="Да":
        await state.update_data(is_sell=callback.data)
        user_dict = await state.get_data()
        info=f"""Город: {user_dict['sell_city']}\n
            Имя: {user_dict['sell_name']}\n
            Телефон: {user_dict['sell_phone']}\n
            Город: {user_dict['sell_city']}\n
            Адрес:{user_dict['']}
            Тип: {user_dict['sell_house']}"""       
        await callback.message.answer('Спасибо, данные записаны!')
        await callback.message.answer('Выберите действие')
        reply_markup=builders.form_without(nedvig.keys()))
        await state.set_state(default_state)
        await callback.answer()
        