from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
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

def get_user_from_database(user_id: int):
    """Возвращает информацию о пользователе по его id"""

    with Session() as session:
        user = session.get(UserBase, user_id)
        return user

def get_subscriptions_from_database():
    """Возвращает базу данных подписок пользователей"""

    with Session() as session:
        # .all() возвращает список всех объектов Users
        subscriptions = session.query(Subscription).all()
        return subscriptions

def add_new_user_to_database(user_name: str, e_mail: str):
    """Добавляет нового пользователя в базу данных. Ответ возвращает в формате JSON."""

    try:
        with Session() as session:

            # Проверяем (email и username должны быть уникальны у каждого пользователя)
            # существует ли уже такой пользователь
            check = session.query(UserBase).filter_by(username=user_name).first()
            if check:
                return {
                    "status": "unsuccess",
                    "username": user_name,
                    "email": e_mail,
                    "msg": "Пользователь с таким именем уже существует"}

            check = session.query(UserBase).filter_by(email=e_mail).first()
            if check:
                return {
                    "status": "unsuccess",
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
                "status": "success",
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                # Форматируем дату как строку: "2026:04:06:20:07"
                "created_at": new_user.created_at.strftime("%d:%m:%Y %H:%M"),
                "msg": "Пользователь создан"}

    except Exception as e:
        print(f"\nОшибка при создании: {e}")
        print("Username:", user_name, "\nemail:", e_mail, "\n")
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})

def delete_user_from_database(user_id):
    """Удаляет пользователя из БД по id"""

    try:
        with Session() as session:
            # Ищем пользователя по первичному ключу (быстрее и безопаснее)
            user = session.get(UserBase, user_id)

            if not user:
                # Пользователь не найден: 404
                return JSONResponse(
                    status_code=404,
                    content={"status": "error", "msg": "Пользователь не найден"}
                )


            session.delete(user)
            session.commit()

            return JSONResponse(
                status_code=200,
                content={"status": "success", "msg": "Пользователь удалён"}
            )

    except Exception as e:
        print(f"\nОшибка при удалении: {e}")
        print("id:", user_id, "\n")

        # Ошибка сервера/БД: 500
        return JSONResponse(
            status_code=500,
            content={"status": "error", "msg": "Внутренняя ошибка сервера"}
        )

def update_user_from_database(user_id: int, new_username: str, new_email: str):
    """Обновляет данные пользователя в БД"""

    try:
        with Session() as session:
            user = session.get(UserBase, user_id)

            if not user:
                return JSONResponse(
                    status_code=404,
                    content={"status": "error", "message": "Пользователь не найден"}
                )

            # Обновляем поля
            user.username = new_username
            user.email = new_email
            user.created_at = datetime.now()

            session.commit()
            print("\nСРАБОТАЛО")
            return {
                "status": "success",
                "message": "Пользователь обновлён",
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.strftime("%d:%m:%Y %H:%M")
            }
        

    except Exception as e:
        print(f"Ошибка обновления: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Ошибка сервера"}
        )

def add_subscription_to_user(user_id: int, currency_id: int):
    """Создаёт новую подписку на валюту для пользователя. Нужен id пользователя и id валюты"""

    try:
        with Session() as session:
            # 1. Проверяем, существует ли пользователь
            user = session.get(UserBase, user_id)
            if not user:
                return JSONResponse(
                    status_code=404,
                    content={"status": "error", "message": "Пользователь не найден"}
                )

            # 2. Проверяем, существует ли валюта
            currency = session.get(Currency, currency_id)  # предполагаем такую модель
            if not currency:
                return JSONResponse(
                    status_code=404,
                    content={"status": "error", "message": "Валюта не найдена"}
                )

            # 3. Проверяем, нет ли уже такой подписки
            existing = session.query(Subscription).filter_by(
                user_id=user_id,
                currency_id=currency_id
            ).first()

            if existing:
                return JSONResponse(
                    status_code=409,  # Conflict
                    content={"status": "error", "message": "Подписка уже существует"}
                )

            # 4. Создаём новую подписку
            new_subscription = Subscription(
                user_id=user_id,
                currency_id=currency_id
            )

            session.add(new_subscription)
            session.commit()
            session.refresh(new_subscription)  # Чтобы получить ID после commit

            # 5. Возвращаем данные для обновления UI
            return {
                "status": "success",
                "message": "Подписка добавлена",
                "user_id": user_id,
                "currency_id": currency_id,
                "currency_code": currency.code,  # например, "USD"
                "currency_name": currency.name,  # например, "Доллар США"
            }

    except IntegrityError as e:
        print(f"Ошибка целостности БД: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Ошибка при создании подписки"}
        )
    except Exception as e:
        print(f"Ошибка при добавлении подписки: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Внутренняя ошибка сервера"}
        )

