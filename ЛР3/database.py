from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from models import Base, Currency, UserBase, Subscription
import requests
from lxml import etree
from fastapi.responses import JSONResponse


# Ссылки
cbr_url = "https://www.cbr.ru/scripts/XML_daily.asp"
DB_URL = "db/database.db"

# Создание движка
engine = create_engine("sqlite:///" + DB_URL, echo=True)

# Создание сессии
Session = sessionmaker(engine)




def create_db_and_tables():
    """Создание всех таблиц"""

    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Ошибка: {e}")

def drop_db_and_tables():
    """Удаление всех таблиц"""

    try:
        Base.metadata.drop_all(engine)
    except Exception as e:
        print(f"Ошибка: {e}")

def get_currencies_cbr():
    """Получаем курсы валют в формате xml от ЦБ РФ"""

    response = requests.get(cbr_url)
    # print(response.text)
    root = etree.fromstring(response.content)
    return root

def fill_currency_table():
    """Заполняем таблицу с валютами"""

    valute = get_currencies_cbr().xpath("//Valute")

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

def get_currencies_from_database():
    """Возвращает базу данных курсов валют"""

    with Session() as session:
        # .all() возвращает список всех объектов Currency
        currencies = session.query(Currency).all()
        return currencies

def get_users_from_database():
    """Возвращает базу данных пользователей"""

    with Session() as session:
        # .all() возвращает список всех объектов Users
        users = session.query(UserBase).all()
        return users

def get_subscriptions_from_database():
    """Возвращает базу данных подписок пользователей"""

    with Session() as session:
        # .all() возвращает список всех объектов Users
        subscriptions = session.query(Subscription).all()
        return subscriptions

def add_new_user_to_database(user_name, e_mail):
    """Добавляет нового пользователя в базу данных. Ответ возвращает в формате JSON."""

    try:
        with Session() as session:

            # Проверяем (email и username должны быть уникальны у каждого пользователя)
            # существует ли уже такой пользователь
            check = session.query(UserBase).filter_by(username=user_name).first()
            if check:
                return {
                    "success": False,
                    "username": user_name,
                    "email": e_mail,
                    "msg": "Пользователь с таким именем уже существует"}

            check = session.query(UserBase).filter_by(email=e_mail).first()
            if check:
                return {
                    "success": False,
                    "username": user_name,
                    "email": e_mail,
                    "msg": "Пользователь с таким email уже существует"}


            # 1. Создаем объект пользователя
            new_user = UserBase(username=user_name, email=e_mail, created_at=datetime.now())

            # 2. Добавляем в сессию (готовим к отправке)
            session.add(new_user)

            # 3. Фиксируем изменения в БД
            session.commit()

            # 4. Отправляем JSON ответ
            return {
                "success": True,
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "created_at": new_user.created_at.isoformat(),
                "msg": "Пользователь создан"}

    except Exception as e:
        print(f"\nОшибка при создании: {e}")
        print("Username:", user_name, "\nemail:", e_mail, "\n")
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
