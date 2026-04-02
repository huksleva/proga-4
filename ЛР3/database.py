from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
from ЛР3.models import Currency
import requests
from lxml import etree


# Создание движка
engine = create_engine('sqlite:///database.db', echo=True)

# Создание сессии
Session = sessionmaker(engine)



# Создание всех таблиц
def create_db_and_tables() -> None:
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Ошибка: {e}")


# Получаем курсы валют в формате xml от ЦБ РФ
def get_currency_valute() -> str:
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    xml_data = response.text
    return xml_data


# Заполняем таблицу с валютами
def add_all_currency_valute():
    try:
        with Session() as session:
            for i in range(10):
                Id = i
                Code = i+10
                Name = "abc"
                record = Currency(id=Id, code=Code, name=Name)

                session.add(record)
                session.commit()
    except Exception as e:
        print(f"Ошибка: {e}")


get_currency_valute()
