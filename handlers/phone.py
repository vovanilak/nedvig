from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from data.states import Anket
from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboard import builders
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove
import os
from dotenv import load_dotenv
from keyboard.builders import *
from data.book import nedvig
from data.states import TELEPHONE
import os
from utils.info import *

router=Router()

@router.message(TELEPHONE.telephone)
async def stage_phone_telephone(message: Message, state: FSMContext):
    await message.answer("Введите ваш номер телефона для обратной связи")
    await state.update_data(tele_name=message.text)
    await state.set_state(TELEPHONE.end)

@router.message(TELEPHONE.end)
async def stage_phone_end(message: Message, state: FSMContext):
    await state.update_data(tele_phone=message.text)
    user_dct = await state.get_data()
    
    add_n_send(
        state='tele',
        chat_id=message.chat.id
    )
    await message.answer(f"Спасибо! Ожидайте нашего звонка")
    await message.answer(
        f"Выберите действие",
        reply_markup=builders.form_without(nedvig.keys())
    )
    await state.update_data(tele_phone=message.text)
    await state.set_state(default_state)




