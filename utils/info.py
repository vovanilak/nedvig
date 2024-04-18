from aiogram.fsm.context import FSMContext
import time
from db.info import *
import os

async def state_info(state_name: str, state: FSMContext):
    a = await state.get_data()
    for_send = 'Ваши данные:'
    for k, v in a.items():
        if k.startswith(state_name):
            for_send += f'\n{v}'
    return for_send

async def add_n_send(
    db_name: str, 
    state: FSMContext, 
    chat_id: int
):
    a = await state.get_data()
    jj = {'chat_id': chat_id, 'time_updated': time.time()}
    tmp = {
        "Аренда недвижимости": "is_arenda",
        "Покупка недвижимости": "is_buy",
        "Продажа недвижимости": "is_sell",
    }
    jj.update(
        {tmp[a['want']]: 1}
    )
    
    for k, v in a.items():
        if k.startswith(db_name):
            jj.update({f'{db_name}_{k.split("_")[1]}': v})
            
    await add_info(jj)

    #for adm in os.getenv('ADMIN').split(','):
    #    await callback.message.bot.send_message(
    #        chat_id=adm, 
    #        text=info,
    #    )