from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, nullable=False)
    name = Column(String(250))
    time_updated = Column(Float)
    want = Column(String(50))

    is_reg=Column(Integer)
    is_buy = Column(Integer) # default=0
    is_sell = Column(Integer)
    is_arenda = Column(Integer)
    is_tele = Column(Integer)

    tele_name = Column(String(100))
    tele_phone = Column(String(20))
    
    reg_name = Column(String(100))
    reg_nomer = Column(String(20))
    reg_city = Column(String(50))
    
    anket_city = Column(String(50))
    anket_house = Column(String(20))
    anket_square = Column(Integer)
    anket_rooms = Column(Integer)
    anket_live = Column(String(200))
    anket_trebovania = Column(String(200))
    anket_money = Column(Integer)
    anket_phone = Column(String(20))
    anket_name = Column(String(50))
    
    sell_city = Column(String(50))
    sell_adress = Column(String(200))
    sell_room = Column(Integer)
    sell_metrage = Column(Integer)
    sell_floor = Column(Integer)
    sell_phone = Column(String(20))
    sell_name = Column(String(50))


def create_table():
    engine = create_engine("sqlite:///data/db.sqlite")
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_table()



