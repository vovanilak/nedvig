from aiogram.fsm.state import State, StatesGroup

class Regre_form(StatesGroup):                   
    number = State()
    city = State()
    info = State()
    end = State()

class Anket(StatesGroup):
    city = State()
    house = State()
    square = State()
    rooms = State()
    live=State()
    trebonia = State()
    money = State()
    number = State()
    name = State()
    info = State()
    end = State()

class Sell(StatesGroup):
    city = State()
    adress = State()
    room = State()
    metrage = State()
    floor = State()
    telephone = State()
    name = State()
    info = State()
    end = State()
    
class TELEPHONE(StatesGroup):
    name = State()
    telephone = State()
    info = State()
    end = State()
