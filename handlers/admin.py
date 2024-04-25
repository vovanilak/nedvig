from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from filters.repeat import CheckAdmin
from keyboard import builders
from db import info
from handlers.start import start_command, start_command_old
from aiogram import F
import os
from aiogram.types.input_file import FSInputFile
router = Router()
router.message(CheckAdmin())

@router.message(Command('full'))
async def cmd_full(message: Message):
    mes = await info.read_table()
    mes = mes.to_string()[:3500]
    await message.answer(mes)


@router.message(Command("admin"))
async def getsecretinfo(message: Message):
    await message.answer(
        text="Администратор, выберите действие",
        reply_markup=builders.form_without([
            "Получить excel",
            "Кому перезвонить",
            "Новые записи",
            "Выход"
        ])
    )

@router.message(F.text.in_((
    "Получить excel",
    "Кому перезвонить",
    "Новые записи",
    )))
async def admin_excel(message: Message):
    if message.text == "Получить excel":
        df = await info.read_table()
        df.to_excel("users.xlsx")
        fl = FSInputFile("users.xlsx")
        await message.bot.send_document(chat_id=message.chat.id, document=fl)
        os.remove("users.xlsx")
    elif message.text == "Кому перезвонить":
        await message.answer('Пока не работает')
    elif message.text == "Новые записи":
        await message.answer('Пока не работает')
    await getsecretinfo(message)


@router.message(F.text=='Выход')
async def admin_exit(message: Message):
    await start_command_old(message)
