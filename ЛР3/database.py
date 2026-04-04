from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from starlette.templating import Jinja2Templates

from models import Base, Currency
import requests
from lxml import etree


# Ссылки
cbr_url = "https://www.cbr.ru/scripts/XML_daily.asp"
DB_URL = "db/database.db"

# Создание движка
engine = create_engine("sqlite:///" + DB_URL, echo=True)

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
    response = requests.get(cbr_url)
    # print(response.text)
    root = etree.fromstring(response.content)
    return root

# Заполняем таблицу с валютами
def add_all_currency_valute():
    valute = get_currency_valute().xpath("//Valute")

    with Session() as session:
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
            session.rollback()

# Добавляем подписку пользователя на валюты
def add_subscription_valute():
    valute = get_currency_valute()

# Возвращает database курсов валют
def get_valute():
    """Возвращает базу данных курсов валют"""

    with Session() as session:
        # .all() возвращает список всех объектов Currency
        currencies = session.query(Currency).all()
        return currencies
