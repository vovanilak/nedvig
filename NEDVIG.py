from aiogram import Bot, Dispatcher, filters, Router, F
from aiogram.filters import StateFilter
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import FSInputFile
from data.book import nedvig
from aiogram import types
import logging
import os
import asyncio
import dotenv
from keyboard.builders import *

dotenv.load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()
user_dict = {}


class Regre_form(StatesGroup):
  nomen = State()
  main = State()
  money = State()


class Anket(StatesGroup):
  sity = State()
  house = State()
  square = State()
  rooms = State()
  live = State()
  trebonia = State()
  Money = State()
  nomber = State()
  named = State()
  info = State()


class seld(StatesGroup):
  CITY = State()
  adres = State()
  room = State()
  metrage = State()
  flor = State()
  telephon = State()
  IMYA = State()
  end = State()


#class BUY(StatesGroup):
class TELETHON(StatesGroup):
  imya = State()
  telephone = State()
  tel = State()
  why = State()


@dp.message(Command('getid'))
async def get_id(message: Message):
  await message.answer(str(message.chat.id))


@dp.message(Command('start'))
async def kso(message: Message, state: FSMContext):
  builder = ReplyKeyboardBuilder()
  btn1 = types.KeyboardButton(text="Аренда недвижимости")
  btn2 = types.KeyboardButton(text="Покупка недвижимости")
  btn3 = types.KeyboardButton(text="Продажа недвижимости")
  btn4 = types.KeyboardButton(text="Задать вопрос")
  btn5 = types.KeyboardButton(text="ТГ канал")
  btn6 = types.KeyboardButton(text="О компании")
  builder.add(btn1, btn2, btn3, btn4, btn5, btn6)
  builder.adjust(2)
  await message.answer(
      "Привет я твой помощник по аренде/продажи/покупки недвижимости.Выберите действие,чтобы зарегистрироваться нажмите команду /register",
      reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.text.in_(nedvig.keys()))
async def book_info(message: types.Message, state: FSMContext):
  txt = message.text
  dct = await state.get_data()
  print(dct)
  if txt in ("Аренда недвижимости", "Покупка недвижимости",
             "Продажа недвижимости") and 'city' in dct:
    await message.answer('Выберите действие.Как вы хотите это сделать❓',
                         reply_markup=inline_kb([
                             "Заказать обратный звонок📱", "Заполнить анкету📕"
                         ]))
  elif txt == "Задать вопрос":
    await message.answer("Перейдите в чат с технической поддержкой📲",
                         reply_markup=inline_btn("Чат с поддержкой💻",
                                                 nedvig["Задать вопрос"]))
  elif txt == "ТГ канал":
    await message.answer("Перейдите в ТГ канал🔔 ",
                         reply_markup=inline_btn("Перейти в тг канал📲",
                                                 "https://t.me/nedvig777"))
  elif txt == "О компании":
    send = nedvig["О компании"]
    await message.answer(send)
  else:
    await message.answer(
        "Для получения информации необходмо пройти регистрацию по команде /register"
    )


    #Продажа недвижимости
@dp.message(F.data.in_("Заполнить анкету📕"))  ########ПРОБЛЕМА
async def ddsjds(message: Message, state: FSMContext):
  await message.answer(
      "Пожалуйста введите данные вашей недвижимости для продажи")


@dp.message(seld.CITY)
async def kdlfkdlfk(message: types.Message, state: FSMContext):
  await message.answer("Введите ваш город")
  await state.update_data(CITYY=message.text)
  await state.set_state(seld.adres)


@dp.message(seld.adres)
async def dfdfkd(message: types.Message, state: FSMContext):
  await message.answer("Введите адрес вашей недвижимости")
  await state.update_data(adress=message.text)
  await state.set_state(seld.room)


@dp.message(seld.room)
async def sdksldk(message: types.Message, state: FSMContext):
  await message.asnwer("Сколько у вас комнат?",
                       reply_murkup=inline_kb["1", "2", "3", "4", "5", "6"])
  await state.set_state(seld.metrage)  #спросить


@dp.callback_query(seld.metrage)
async def sdjksj(callback: CallbackQuery, state: FSMContext):
  await callback.message.answer("Сколько метров у вашей недвижимости?")
  await state.update_data(metragee=callback.message.text)
  await state.set_state(seld.flor)


@dp.message(seld.flor)
async def dfkdslfdf(message: types.Message, state: FSMContext):
  await message.answer("Сколько у вас этажей?",
                       reply_markup=inline_kb["1", "2", "3", "4"])
  await state.update_data(florr=message.text)
  await state.set_state(seld.telephon)


@dp.callback_query(seld.telephon)
async def fldjsfja(callback: CallbackQuery, state: FSMContext):
  await callback.message.answer("Введите ваш номер телефона")
  await state.update_data(telethonn=callback.message.text)
  await state.set_state(seld.IMYA)


@dp.message(seld.IMYA)
async def ddkfdfd(message: Message, state: FSMContext):
  await message.answer("Введите имя")
  await state.update_data(IMYAA=message.text)
  await state.set_state(seld.end)


@dp.message(seld.end)
async def end_state(message: Message, state: FSMContext):
  await message.answer(
      "Ваша заявка принята,спасибо!Чтобы посмотреть данные вашей регистрации нажмите на команду /see,а чтобы выйти в лобби нажмите команду /cancel"
  )
  await state.update_data(endd=message.text)
  await state.set_state(default_state())


@dp.callback_query(F.data.in_(("Заказать обратный звонок📱")))
async def djfdjiffdj(callback: CallbackQuery, state: FSMContext):
  await callback.message.answer("Введите имя")
  await state.update_data(imyaa=callback.message.text)
  await state.set_state(TELETHON.telephone)


@dp.message(TELETHON.telephone)
async def jrigrjghig(message: Message, state: FSMContext):
  await message.answer("Введите ваш номер телефона для обратной связи")
  await state.update_data(telethonee=message.text)
  await state.set_state(TELETHON.tel)


@dp.message(TELETHON.tel)
async def tel_state(message: Message, state: FSMContext):
  await message.answer(f"Номер верный?\n{message.text}",
                       reply_markup=inline_kb(["Да", "Нет"]))
  await state.update_data(tell=message.text)
  await state.set_state(TELETHON.why)

@dp.callback_query(TELETHON.why)
async def sjdsjdksjk(callback: CallbackQuery, state: FSMContext):
  await callback.message.answer(f"Ваш номер верный?\n{callback.message.text}")

@dp.message(filters.StateFilter(TELETHON.why))
async def age_state(message, state):
  await state.update_data(know=message.text)
  await message.answer('Спасибо! Ваши данные сохранены!\n\n'
                       'Вы вышли из регистрации')
  await message.answer('Чтобы посмотреть данные вашей '
                       'анкеты - отправьте команду /look')
  await state.set_state(default_state)


@dp.message(filters.Command("look"), filters.StateFilter(default_state))
async def showdata(MSG):
  infoo = f"Имя: {user_dict[MSG.from_user.id]['name']}\n\
Телефон:{user_dict[MSG.from_user.id]['nomer']}"

  await MSG.answer(infoo)

  #resume={}
  #dct=await state.get_data()
  #for dddd in ["imyaa","telethonee"]:
  #resume.update({dddd:dct[dddd]})
  #await bot.send_message(chat_id=int(os.getenv('ADMIN')), text=str(resume))


@dp.callback_query(F.data.in_(("Заполнить анкету📕")))
async def ggg(callback: CallbackQuery, state: FSMContext):
  await callback.message.answer("Пожалуйста введите ваш город")
  await state.set_state(Anket.sity)


@dp.message(filters.StateFilter(Anket.sity))
async def name(message: types.Message, state: FSMContext):
  await state.update_data(ccity=message.text)
  await message.answer("Спасибо,интересует квартира или дом?",
                       reply_markup=inline_kb(["Квартира", "Дом"]))
  await state.set_state(Anket.house)


@dp.callback_query(Anket.house, F.data.in_(["Квартира", "Дом"]))
async def dded(callback: CallbackQuery, state: FSMContext):
  await state.update_data(housee=callback.data)
  await callback.message.answer("Введите площадь")
  await callback.answer()  #убрать загрузку кнопки
  await state.set_state(Anket.square)


@dp.message(Anket.house)
async def dded_error(message: Message):
  await message.answer("Такого варианта нет,повторите попытку",
                       reply_markup=inline_kb(["Квартира", "Дом"]))


@dp.message(Anket.square)
async def sddd(message: types.Message, state: FSMContext):
  await message.answer("Сколько комнат?",
                       reply_markup=inline_kb(['1', '2', '3', '4', '5', '6']))
  await state.update_data(roomss=message.text)
  await state.set_state(Anket.live)


@dp.callback_query(F.data.in_(['1', '2', '3', '4', '5', '6']), Anket.live)
async def dds(callback: CallbackQuery, state: FSMContext):
  await callback.message.answer("Для кого недвижимость? Кто будет проживать?")
  await state.update_data(livee=callback.message.text)
  await state.set_state(Anket.trebonia)


@dp.message(Anket.live)
async def dded_error(message: Message):
  await message.answer("Такого варианта нет,повторите попытку",
                       reply_markup=inline_kb(['1', '2', '3', '4', '5', '6']))


@dp.message(Anket.trebonia)
async def djfijf(message: Message, state: FSMContext):
  await message.answer("Какие требования у вас есть к объекту?"
                       )  ###добавить кнопку инлайн
  await state.update_data(trebovaniaa=message.text)
  await state.set_state(Anket.Money)


@dp.message(Anket.Money)
async def pfefk(message: Message, state: FSMContext):
  await message.answer("Какой у вас бюджет?Укажите только цифрами🔢")
  await state.update_data(Moneyy=message.text)
  await state.set_state(Anket.nomber)


@dp.message(Anket.nomber, F.text.isdigit())
async def edeofeokd(message: Message, state: FSMContext):
  await message.answer("Введите свой номер телефона")
  await state.update_data(nomderr=message.text)
  await state.set_state(Anket.named)


@dp.message(Anket.nomber)
async def dkddf(message):
  await message.answer("Данные не правильные,повторите попытку")


@dp.message(Anket.named)
async def dfjfke(message: Message, state: FSMContext):
  await message.answer("Введите имя")
  await state.update_data(nameeee=message.text)
  await state.set_state(Anket.info)

  #result={}
  #dct=await state.get_data()
  #for dddd in ["ccity","housee","roomss","livee","trebovaniaa","Moneyy","nomderr","nameeee"]:
  #result.update({dddd:dct[dddd]})
  #await bot.send_message(chat_id=int(os.getenv('ADMIN')), text=str(result))
  #await message.answer("Спасибо с вами скоро свяжутся,нажмите команду /saw,чтобы увидеть данные вашей регистрации")


@dp.message(filters.StateFilter(Anket.info))
async def name_state(message, state):
  await state.update_data(namee=message.text)
  #user_dict[message.from_user.id]=await state.get_data()
  await state.clear()
  await message.answer('Спасибо! Ваши данные сохранены!\n\n'
                       'Вы вышли из регистрации')
  await message.answer('Чтобы посмотреть данные вашей '
                       'анкеты - отправьте команду /see')
  await message.answer("Выберите действие",
                       reply_markup=form_without(nedvig.keys())
                       )  ###Вызов основного меню
  await state.set_state(default_state)


@dp.message(filters.Command("see"), filters.StateFilter(default_state))
async def showdata(message: Message, state: FSMContext):
  '''#infoo=f"Город: {user_dict[MSG.from_user.id]['']}\n\
:{user_dict[MSG.from_user.id]['']}\n\
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}
:{user_dict[MSG.from_user.id]['']}'''

  #await MSG.answer(infoo)
  await message.answer("Выберите действие",
                       reply_markup=form_without(nedvig.keys()))


@dp.message(filters.Command("cancel"), ~filters.StateFilter(default_state))
async def default_cancel(MSG, state):
  await MSG.answer("'Вы вышли из регистрации'"
                   'Чтобы снова перейти к заполнению анкеты - '
                   "'отправьте команду /register'")


@dp.message(filters.Command("cancel"), filters.StateFilter(default_state))
async def default_cancel(MSG):
  await MSG.answer("отменять нечего,введите команду /register")


@dp.message(filters.Command("register"))
async def mess(message: Message, state: FSMContext):
  await message.answer("Привет, пожалуйста пройди регистрацию")
  await message.answer(text='Пожалуйста, введите ваше имя')
  await state.set_state(Regre_form.nomen)


@dp.message(filters.StateFilter(Regre_form.nomen), F.text.isalpha())
async def reg_phone(message: types.Message, state: FSMContext):
  await state.update_data(name=message.text)
  await message.answer("Спасибо,введите свой номер телефона")
  await state.set_state(Regre_form.main)


@dp.message(filters.StateFilter(Regre_form.main))
async def reg_city(message: types.Message, state: FSMContext):
  await state.update_data(nomer=message.text)
  await message.answer("Спасибо,введите название своего города")
  await state.set_state(Regre_form.money)


@dp.message(filters.StateFilter(Regre_form.money))
async def age_state(message, state):
  await state.update_data(city=message.text)
  await message.answer('Спасибо! Ваши данные сохранены!\n\n'
                       'Вы вышли из регистрации')
  await message.answer('Чтобы посмотреть данные вашей '
                       'анкеты - отправьте команду /see')
  await state.set_state(default_state)


@dp.message(filters.Command("see"), filters.StateFilter(default_state))
async def showdata(MSG):
  info = f"Имя: {user_dict[MSG.from_user.id]['name']}\n\
Телефон:{user_dict[MSG.from_user.id]['nomer']}\n\
Город:{user_dict[MSG.from_user.id]['city']}"

  await MSG.answer(info)


async def main():
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())
