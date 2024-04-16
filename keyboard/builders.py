from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram import types
def form(frog):
    builder2 = ReplyKeyboardBuilder()
    for j in frog:
        builder2.add(types.KeyboardButton(text=j))
    builder2.add(types.KeyboardButton(text="Назад"))
    return builder2.adjust(2).as_markup(resize_keyboard=True)# resize_keyboard-изменяет размер клавиатуры
def form_without(frog):
    builder2 = ReplyKeyboardBuilder()
    for j in frog:
        builder2.add(types.KeyboardButton(text=j))
    return builder2.adjust(2).as_markup(resize_keyboard=True)# resize_keyboard-изменяет размер клавиатуры
def inline_btn(txt,ur):
    builder=InlineKeyboardBuilder()
    builder.button(text=txt,url=ur)
    return builder.as_markup()
def inline_kb(btns):
    builder=InlineKeyboardBuilder()
    for f in btns:
        builder.button(text=f,callback_data=f)
    return builder.adjust(3).as_markup()