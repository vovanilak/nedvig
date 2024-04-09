from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

class CheckRepeat(Filter):
    def __init__(self, stage):#переменные каторые будут использоваться в других методов
        self.stage=stage
    async def __call__ (self, message: Message, state: FSMContext):#действия после вызова класса.
        data = await state.get_data()#получение всего хранилища
        return self.stage in data.keys()#проверяет определенные ключи в хранилище(словарик).
        
        