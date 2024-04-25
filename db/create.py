from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, nullable=False)
    name = Column(String(250))
    time_updated = Column(Float)
    want = Column(String(50))

    is_reg=Column(Boolean, default=False)
    is_buy = Column(Boolean, default=False) # default=0
    is_sell = Column(Boolean, default=False)
    is_arenda = Column(Boolean, default=False)
    is_tele = Column(Boolean, default=False)

    tele_name = Column(String(100))
    tele_phone = Column(String(20))
    
    reg_name = Column(String(100))
    reg_nomer = Column(String(20))
    reg_city = Column(String(50))
    
    arenda_city = Column(String(50))
    arenda_house = Column(String(20))
    arenda_square = Column(Integer)
    arenda_rooms = Column(Integer)
    arenda_live = Column(String(200))
    arenda_trebovania = Column(String(200))
    arenda_money = Column(Integer)
    arenda_phone = Column(String(20))
    arenda_name = Column(String(50))

    buy_city = Column(String(50))
    buy_house = Column(String(20))
    buy_square = Column(Integer)
    buy_rooms = Column(Integer)
    buy_live = Column(String(200))
    buy_trebovania = Column(String(200))
    buy_money = Column(Integer)
    buy_phone = Column(String(20))
    buy_name = Column(String(50))
    
    sell_city = Column(String(50))
    sell_adress = Column(String(200))
    sell_room = Column(Integer)
    sell_metrage = Column(Integer)
    sell_floor = Column(Integer)
    sell_phone = Column(String(20))
    sell_name = Column(String(50))

    admin_arenda = Column(Boolean, default=False)
    admin_buy = Column(Boolean, default=False)
    admin_sell = Column(Boolean, default=False)


def create_table():
    engine = create_engine("sqlite:///data/db.sqlite")
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_table()



