from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.create import Users
import pandas as pd
from sqlalchemy import update

async def read_table():
    engine = create_engine("sqlite:///data/db.sqlite")
    Session = sessionmaker(bind=engine)
    s = Session()
    df = pd.read_sql_table('users', engine)
    s.close()
    return df

async def add_info(dct: dict):
    engine = create_engine("sqlite:///data/db.sqlite")
    Session = sessionmaker(bind=engine)
    s = Session()
    result = s.query(Users).filter(Users.chat_id == dct['chat_id']).first()
    if result:
        u = update(Users).values(dct)
        s.execute(u)
        #s.query(Users).filter_by(chat_id=dct['chat_id']).update(dct)
    else:
        hero = Users(**dct)
        s.merge(hero)
    s.commit()
    s.close()