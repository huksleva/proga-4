from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
from ЛР3.models import Currency
import requests
from lxml import etree


# Создание движка
engine = create_engine('sqlite:///db/database.db', echo=True)

# Создание сессии
Session = sessionmaker(engine)



# Создание всех таблиц
def create_db_and_tables() -> None:
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Ошибка: {e}")


# Удаление всех таблиц
def drop_db_and_tables() -> None:
    try:
        Base.metadata.drop_all(engine)
    except Exception as e:
        print(f"Ошибка: {e}")

# Получаем курсы валют в формате xml от ЦБ РФ
def get_currency_valute():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    # print(response.text)
    root = etree.fromstring(response.content)
    return root


# Заполняем таблицу с валютами
def add_all_currency_valute():
    valute = get_currency_valute().xpath("//Valute")
    session = Session()

    try:
        # Работает с неймспейсами: ищет элементы по локальному имени
        for i, el in enumerate(valute):

            # Получаем нужные нам данные из XML
            name_el = el.find("Name").text
            # id_value = el.get("ID")
            code_el = el.find("CharCode").text

            # Формируем ответ
            record = Currency(
                id=i,
                code=code_el,
                name=name_el
            )

            # Добавляем новую запись в БД
            session.add(record)

        # Логирование
        session.commit()

    except Exception as e:
        print(f"Ошибка: {e}")
        Session().rollback()

