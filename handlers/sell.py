from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from data.states import Anket
from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboard.builders import inline_kb
import os
from dotenv import load_dotenv
from keyboard.builders import *
from data.book import nedvig
from data.states import Sell
from filters.repeat import CheckRepeat
from db.info import *
from dotenv import load_dotenv
import time

load_dotenv()
#from handlers.arenda_buy import info
router=Router()

@router.message(Sell.city)
async def stage_anket_city(message: Message, state: FSMContext):
    await state.update_data(sell_city=message.text)
    await state.set_state(Sell.adress)
    await message.answer("Введите адрес вашей недвижимости")

@router.message(Sell.adress)
async def stage_anket_adress(message: Message, state: FSMContext):
    await state.update_data(sell_adress=message.text)
    await state.set_state(Sell.room)
    await message.answer(text="Сколько у Вас комнат?",
                         reply_markup=inline_kb(["1", "2", "3", "4", "5", "6"]))

@router.callback_query(Sell.room, F.data.in_(["1", "2", "3", "4", "5", "6"]))
async def stage_anket_room(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(sell_room=int(callback.data))
    await state.set_state(Sell.metrage)
    await callback.message.answer(
        "Сколько метров у Вашей недвижимости (введите число в квадратных метрах)?"
    )

@router.callback_query(Sell.room)
async def stage_anket_room_error(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Нажмите на одну из кнопок')
    await callback.message.asnwer(text="Сколько у Вас комнат?",
                                  reply_murkup=inline_kb(["1", "2", "3", "4", "5", "6"]))
    
@router.message(Sell.metrage, F.text.isdigit())
async def stage_anket_metrage(message: Message, state: FSMContext):
    await state.update_data(sell_metrage=int(message.text))
    await state.set_state(Sell.floor)
    await message.answer(text="Сколько у вас этажей (введите цифру)?")

@router.message(Sell.metrage)
async def stage_anket_metrage_error(message: Message):
    await message.answer(text="ошибка, вы используете буквы,Сколько у вас этажей (введите цифру в квадратных метрах)?")

@router.message(Sell.floor, F.text.isdigit())
async def stage_anket_floor(message: Message, state: FSMContext):
    await state.update_data(sell_floor=int(message.text))
    await state.set_state(Sell.telephone)
    await message.answer("Введите ваш номер телефона")

@router.message(Sell.floor)
async def stage_anket_floor_error(message: Message):
    await message.answer(text="ошибка,Сколько у вас этажей (введите цифру)?")

@router.message(Sell.telephone)
async def stage_anket_telephone(message: Message, state: FSMContext):
    await state.update_data(sell_phone=message.text)
    await state.set_state(Sell.name)
    await message.answer("Введите Ваше имя")

@router.message(Sell.name)
async def stage_anket_name(message: Message, state: FSMContext):
    await state.update_data(sell_name=message.text)
    await state.set_state(Sell.info)
    user_dict = await state.get_data()
    info=f"""Адрес: {user_dict['sell_city']}\n
Адрес2: {user_dict['sell_adress']}\n
Комнаты: {user_dict['sell_room']}\n
Метраж: {user_dict['sell_metrage']}\n
Этажи: {user_dict['sell_floor']}\n        
Имя: {user_dict['sell_name']}\n
Телефон:{user_dict['sell_phone']}"""
    await message.answer(f'Данные верны?\n{info}', 
                         reply_markup=inline_kb(('Верны', 
                                                 'Есть ошибка')))

    
@router.callback_query(Sell.info, F.data.in_(['Верны','Есть ошибка']))
async def sell_end(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Верны':
        await state.update_data(is_sell=1)
        user_dict = await state.get_data()
        info=f"""Адрес: {user_dict['sell_city']}\n
Адрес2: {user_dict['sell_adress']}\n
Комнаты: {user_dict['sell_room']}\n
Метраж: {user_dict['sell_metrage']}\n
Этажи: {user_dict['sell_floor']}\n        
Имя: {user_dict['sell_name']}\n
Телефон:{user_dict['sell_phone']}"""
        
        jj = {'is_sell': 1, 'chat_id': int(callback.message.chat.id), 'time_updated': time.time()}
        for k, v in user_dict.items():
            if k.startswith('sell'):
                jj.update({k: v})

        await add_info(jj)
        #await callback.message.answer(await read_table())
        for adm in os.getenv('ADMIN').split(','):
            await callback.message.bot.send_message(
                chat_id=adm, 
                text=info,
            )
        await callback.message.answer('Спасибо, данные записаны!')
        await callback.message.answer('Выберите действие',
                                      reply_markup=form_without(nedvig.keys()))
        await state.set_state(default_state)
        await callback.answer()
    else:
        await callback.message.answer('Пожалуйста, заполние анкету ещё раз')
        await callback.message.answer("Пожалуйста введите город продажи")
        await state.set_state(Sell.city)
        await callback.answer()

@router.callback_query(Sell.info)
async def sell_end_error(callback: CallbackQuery):
    await callback.message.answer(text=f'Пожалуйста, выберите одну из кнопок:',
                                  reply_markup=inline_kb(('Верно', 'Есть ошибка')))


