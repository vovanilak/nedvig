from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from data.states import Anket
from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboard import builders
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from filters.repeat import CheckRepeat
import os
from dotenv import load_dotenv
from keyboard.builders import *
from data.book import nedvig
from db.info import *
import time
from utils.info import *

load_dotenv()

router = Router()

@router.message(Anket.city)
async def stage_anket_city(message: Message, state: FSMContext):
    await state.set_state(Anket.house)
    await state.update_data(anket_city=message.text)
    await message.answer("Спасибо, интересует квартира или дом?",
                         reply_markup=inline_kb(["Квартира","Дом"]))

@router.callback_query(Anket.house, F.data.in_(["Квартира","Дом"]))
async def stage_anket_house(callback: CallbackQuery, state: FSMContext):
    await state.update_data(anket_house=callback.data)
    await callback.message.answer("Введите площадь в квадратных метрах. Укажите цифрами🔢")
    await callback.answer()#убрать загрузку кнопки
    await state.set_state(Anket.square)
    
@router.message(Anket.house)
async def stage_anket_house_error(message: Message):
    await message.answer("Такого варианта нет,повторите попытку",
                         reply_markup=inline_kb(["Квартира","Дом"]))
    
@router.message(Anket.square,F.text.isdigit())
async def stage_anket_square(message: Message, state: FSMContext):
    await state.set_state(Anket.live)
    await message.answer("Сколько комнат?",
                         reply_markup=inline_kb(['1','2','3','4','5','6']))
    await state.update_data(anket_square=message.text)

@router.message(Anket.square)
async def stage_anket_square_error(message: Message):
    await message.answer("Нужно использовать только цифры,введите еще раз.")
    
@router.callback_query(Anket.live, F.data.in_(['1','2','3','4','5','6']))
async def stage_anket_live(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Для кого недвижимость? Кто будет проживать?")
    await state.update_data(anket_rooms=int(callback.data))
    await callback.answer()
    await state.set_state(Anket.trebonia)
    
@router.message(Anket.live)
async def stage_anket_live_error(message: Message):
    await message.answer("Такого варианта нет,повторите попытку",
                         reply_markup=inline_kb(['1','2','3','4','5','6']))
    
@router.message(Anket.trebonia)
async def stage_anket_trebonia(message: Message, state: FSMContext):
    await message.answer("Какие требования у вас есть к объекту?")###добавить кнопку инлайн
    await state.update_data(anket_live=message.text)
    await state.set_state(Anket.money)
    
@router.message(Anket.money)
async def stage_anket_money(message: Message, state: FSMContext):
    await message.answer(
        text="Какой у вас бюджет? Напишите в тысячах, например, 2 млн = 2 000 тыс. Укажите цифрами🔢"
    )
    await state.update_data(anket_trebovania=message.text)
    await state.set_state(Anket.number)

@router.message(Anket.number, F.text.isdigit())
async def stage_anket_number(message: Message, state: FSMContext):
    await message.answer("Введите свой номер телефона в формате +79999999999")
    await state.update_data(anket_money=int(message.text))
    await state.set_state(Anket.name)
    
@router.message(Anket.number)
async def stage_anket_number_error(message):
    await message.answer("Данные неправильные, повторите попытку")
    
@router.message(
    Anket.name,
    F.text.startswith("+"), 
    F.text[1:].isdigit(),
)
async def stage_anket_name(message: Message, state: FSMContext):
    await message.answer("Введите имя")
    await state.update_data(anket_phone=message.text[1:])
    await state.set_state(Anket.info)

@router.message(Anket.name)
async def stage_phone_error(message: Message):
    await message.answer("Данные неправильные, повторите попытку. Формат: +79999999999"
    'Минимум 10 символов, номер должен начинаться с +')

@router.message(Anket.info)
async def stage_anket_info(message,state):
    await state.update_data(anket_name=message.text)
    #user_dict[message.from_user.id]=await state.get_data()
    user_dict = await state.get_data()
    info = await state_info('anket', state)
    await message.answer(text=f'Спасибо! Пожалуйста, проверьте данные и нажмите кнопку:\n\n{info}',
                    reply_markup=builders.inline_kb(('Верно', 'Неверно')))
    await state.set_state(Anket.end)

@router.callback_query(Anket.end, F.data.in_(['Верно','Неверно']))
async def end_anket(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Верно':
        user_dict = await state.get_data()
        await add_n_send(state=state, chat_id=int(callback.message.chat.id))
        await callback.message.answer('Спасибо, данные записаны!')
        await callback.message.answer('Выберите действие',
                                      reply_markup=builders.form_without(nedvig.keys()))
        await state.set_state(default_state)
        await callback.answer()
    else:
        await callback.message.answer('Пожалуйста, заполние анкету ещё раз')
        await callback.message.answer("Пожалуйста введите город")
        await state.set_state(Anket.city)
        await callback.answer()

@router.callback_query(Anket.end)
async def end_anket_error(callback: CallbackQuery):
    await callback.message.answer(text=f'Пожалуйста, выберите одну из кнопок:',
        reply_markup=builders.inline_kb(('Верно', 'Неверно')))



