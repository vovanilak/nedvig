from aiogram.filters import Command
from aiogram import types,Router,F
from data.book import nedvig
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboard import builders
from filters.repeat import CheckRepeat
from aiogram.fsm.state import default_state
from aiogram.filters import and_f, or_f

router=Router()

#router.message.middleware(CheckRegistration())
#фильтр на не зарегистрированных пользователей

@router.message(Command('getid'))
async def get_id(message: Message):
    await message.answer(str(message.chat.id))

@router.message(
    ~CheckRepeat('is_reg'), 
    Command('start')
)
async def start_command(message: Message):
    await message.answer(
        text='Добро пожаловать! Это бот по продаже, покупке и аренде недвиижмости ',
        reply_markup=builders.form_without((
        'ТГ канал', "Задать вопрос", "О компании", "Регистрация"))
    )

@router.message(CheckRepeat('is_reg'), Command('start'))
async def start_command_old(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(
        text='Это бот такой-то. Потом напишу. Выберите действие',
        reply_markup=builders.form_without(nedvig.keys())
    )
    
    
