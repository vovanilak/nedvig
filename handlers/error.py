from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

router = Router()

@router.message()
async def main_error(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer("Что-то пошло не так. Воспользуйтесь /start")

@router.callback_query()
async def end_anket(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    await callback.message.answer("Что-то пошло не так. Воспользуйтесь /start")