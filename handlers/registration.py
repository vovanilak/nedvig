from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from data.states import Regre_form
from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboard import builders
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove
import os
import time
from data.book import nedvig
from dotenv import load_dotenv

from db.info import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from keyboard.builders import form_without

load_dotenv()

router = Router()

@router.message(Regre_form.number)
async def reg_phone(message: Message, state: FSMContext):
    await state.update_data(reg_name=message.text)
    await message.answer("Спасибо, введите свой номер телефона")
    await state.set_state(Regre_form.city)
    
@router.message(Regre_form.city)
async def reg_city(message: Message, state: FSMContext):
    await state.update_data(reg_nomer=message.text)
    await message.answer("Спасибо, введите название своего города")
    await state.set_state(Regre_form.info)
    
@router.message(Regre_form.info)
async def age_state(message,state):
    await state.update_data(reg_city=message.text)
    user_dict = await state.get_data()
    info=f"Имя: {user_dict['reg_name']}\nТелефон:{user_dict['reg_nomer']}\nГород:{user_dict['reg_city']}"
    await message.answer(text=f'Спасибо! Пожалуйста, проверьте данные и нажмите кнопку:\n\n{info}',
                        reply_markup=builders.inline_kb(('Верно', 'Неверно')))           
    await state.set_state(Regre_form.end)

@router.callback_query(Regre_form.end)
async def reg_end(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == 'Верно':
        await state.update_data(is_reg=1)
        user_dict = await state.get_data()
        info=f"Имя: {user_dict['reg_name']}\nТелефон:{user_dict['reg_nomer']}\nГород:{user_dict['reg_city']}"
        ch_id = int(callback.message.chat.id)
        await add_info(
            {
                'chat_id': ch_id,
                'reg_name': user_dict['reg_name'],
                'reg_nomer': user_dict['reg_nomer'],
                'reg_city': user_dict['reg_city'],
                'is_reg': 1,
                'time_updated': time.time()
            }
        )

        #for k, v in user_dict.items():
        #    if k.startswith('reg'):
        #await callback.message.answer(str(s.query(Users).all()[0].id))
        #await callback.message.bot.send_message(chat_id=os.getenv('ADMIN'), text=info)
        await callback.message.answer('Спасибо, вы успешно зарегистрировались!')
        await callback.message.answer('Выберите действие',
                                      reply_markup=builders.form_without(nedvig.keys()))
        await state.set_state(default_state)
        await callback.answer()
    else:
        await callback.message.answer('Пожалуйста, пройдите регистрацию ещё раз')
        await callback.message.answer('Введите Ваше имя')
        await state.set_state(Regre_form.number)
        await callback.answer()
