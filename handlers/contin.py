from data.states import Anket, TELEPHONE, Sell, Regre_form
from aiogram import Router, F
from data.book import nedvig
from aiogram.types import Message, CallbackQuery
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from filters.repeat import CheckRepeat
from keyboard.builders import *
from data.book import nedvig
from aiogram.filters import or_f, and_f

router=Router()

@router.message(
    F.text.in_((
        "Задать вопрос",
        "ТГ канал",
        "О компании",
        "Регистрация"
    ))
)
async def book_info(message: Message,state: FSMContext):
    txt=message.text
    if txt == "Задать вопрос":
        await message.answer("Перейдите в чат с технической поддержкой📲", 
                reply_markup=inline_btn("Чат с поддержкой💻",
                                        nedvig["Задать вопрос"]))
    elif txt =="ТГ канал":
        await message.answer("Перейдите в ТГ канал🔔 ", 
                reply_markup=inline_btn("Перейти в тг канал📲",
                                        "https://t.me/nedvig777"))
    elif txt == "О компании":
        send=nedvig["О компании"]
        await message.answer(send)
        
    elif message.text  == "Регистрация":
        await state.set_state(Regre_form.number)
        await message.answer(text="Пожалуйста, пройдите регистрацию", 
                            reply_markup=ReplyKeyboardRemove())
        await message.answer(text='Введите Ваше имя')
    
@router.message(
    CheckRepeat('is_reg'),
    or_f(
        and_f(
            CheckRepeat('is_arenda'),
            F.text == "Аренда недвижимости"     
        ),
        and_f(
            CheckRepeat('is_buy'),
            F.text == "Покупка недвижимости"     
        ),
        and_f(
            CheckRepeat('is_sell'),
            F.text == "Продажа недвижимости"
        )
    )
)
async def ask_rewrite(message: Message, state: FSMContext):
    await state.update_data(want=message.text)
    await message.answer(text="Ваши данные уже сохранены, Вы хотите их перезаписать?",
                        reply_markup=inline_kb(["Перезаписать", 
                                                "Отмена"]))

@router.callback_query(
    CheckRepeat('is_reg'), 
    F.data.in_(["Перезаписать", "Отмена"])
)
async def rewrite_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "Перезаписать":
        await stage_continue_old(callback.message, state)
        '''
        a = await state.get_data()
        if a['want'] in ("Аренда недвижимости", "Покупка недвижимости"):
            await state.set_state(Anket.city)
        elif a['want'] == "Продажа недвижимости":
            await state.set_state(Sell.city)
        await callback.message.answer(text='Перевожу на анкетирование',
                                     reply_markup=ReplyKeyboardRemove())
        await callback.message.answer('Пожалуйста, введите город')
        '''
    elif callback.data == "Отмена":
        await callback.message.answer('Перевожу на главное меню')
        await callback.message.answer(text='Выберите действие',
                                      reply_markup=form_without(nedvig.keys()))

        
@router.message(
    CheckRepeat('is_reg'),
    or_f(
        and_f(
            ~CheckRepeat('is_arenda'),
            F.text == "Аренда недвижимости"     
        ),
        and_f(
            ~CheckRepeat('is_buy'),
            F.text == "Покупка недвижимости"
        ),
        and_f(
            ~CheckRepeat('is_sell'),
            F.text == "Продажа недвижимости"
        )
    )
)
async def stage_continue_old(message: Message, state: FSMContext):
    txt=message.text
    await state.update_data(want=txt)
    await message.answer(text='Выберите действие. Как Вы хотите это сделать❓',
                             reply_markup=inline_kb(["Заказать звонок📱",
                                                     "Заполнить анкету📕"]))

@router.callback_query(
    CheckRepeat('is_reg'), 
    F.data == "Заполнить анкету📕"
)
async def ask_continue_old(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    a = await state.get_data()
    if a['want'] in ("Аренда недвижимости", "Покупка недвижимости"):
        await state.set_state(Anket.city)
        await callback.message.answer("Пожалуйста, введите город аренды/покупки",
                                     reply_markup=ReplyKeyboardRemove())

    elif a['want'] == "Продажа недвижимости":
        await state.set_state(Sell.city)
        await callback.message.answer("Пожалуйста, введите город продажи",
                                     reply_markup=ReplyKeyboardRemove())

@router.callback_query(
    CheckRepeat('is_reg'),
    F.data == "Заказать звонок📱"
)
async def phone_continue_old(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(TELEPHONE.telephone)
    await callback.message.answer("Введите имя",
                                 reply_markup=ReplyKeyboardRemove())
    




