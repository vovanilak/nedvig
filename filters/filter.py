from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

class CheckRegistration(Filter):
    def __init__(self, my_text):
        self.my_text = my_text

    async def __call__(self, message: Message, state: FSMContext):
        data = await state.get_data()
        return self.my_text in data.keys()
        
    