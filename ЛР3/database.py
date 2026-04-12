from sqlalchemy.orm import sessionmaker, Session
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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Функция-генератор зависимости"""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

    try:
        with SessionLocal() as session:
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


def get_currencies_from_database(db: Session):
    """Возвращает базу данных курсов валют"""

    currencies = db.query(Currency).all()
    return currencies


def get_users_from_database(db: Session):
    """Возвращает базу данных пользователей"""

    users = db.query(UserBase).all()
    return users


def get_user_from_database(user_id: int, db: Session):
    """Возвращает информацию о пользователе по его id"""

    user = db.get(UserBase, user_id)
    return user


def get_subscriptions_from_database(db: Session):
    """Возвращает базу данных подписок пользователей"""

    subscriptions = db.query(Subscription).all()
    return subscriptions


def add_new_user_to_database(user_name: str, e_mail: str, db: Session):
    """Добавляет нового пользователя в базу данных. Ответ возвращает в формате JSON."""

    try:
        # Проверяем (email и username должны быть уникальны у каждого пользователя)
        # Если пользователь уже существует
        if db.query(UserBase).filter_by(username=user_name).first():
            return None
        # Если почта уже существует
        if db.query(UserBase).filter_by(email=e_mail).first():
            return None

        # 1. Создаем объект пользователя
        # Форматируем дату как строку: "2026:04:06 20:07"
        new_user = UserBase(
            username=user_name,
            email=e_mail,
            created_at=datetime.now().strftime("%d:%m:%Y %H:%M"))

        # 2. Добавляем в сессию (готовим к отправке)
        db.add(new_user)

        # 3. Фиксируем изменения в БД
        db.commit()

        # 4. Важно, чтобы получить id после commit
        db.refresh(new_user)

        # 5. Отправляем ответ
        return new_user

    except Exception as e:
        print(f"Критическая ошибка БД: {e}")
        return None


def update_user_from_database(user_id: int, new_username: str, new_email: str, db: Session):
    """Обновляет данные пользователя в БД"""

    try:
        updatetable_user = db.get(UserBase, user_id)

        if not updatetable_user:
            return None  # Сигнал роуту: пользователь не найден

        # Обновляем данные
        updatetable_user.username = new_username
        updatetable_user.email = new_email

        db.commit()
        db.refresh(updatetable_user)  # Синхронизируем объект с БД после коммита

        return updatetable_user

    except Exception as e:
        db.rollback()
        print(f"Ошибка обновления: {e}")
        raise RuntimeError("Ошибка сервера при обновлении")


def add_subscription_to_user(user_id: int, currency_id: int, db: Session):
    """Создаёт новую подписку на валюту для пользователя. Нужен id пользователя и id валюты"""

    try:
        # 1. Проверяем, существует ли пользователь
        if not db.get(UserBase, user_id):
            return None

        # 2. Проверяем, существует ли валюта
        if not db.get(Currency, currency_id):
            return None

        # 3. Проверяем, нет ли уже такой подписки. Проверяем по уникальному ключу
        if db.get(Subscription, (user_id, currency_id)):
            return None

        # 4. Создаём новую подписку
        new_subscription = Subscription(
            user_id=user_id,
            currency_id=currency_id
        )

        # 5. Добавляем в сессию (готовим к отправке)
        db.add(new_subscription)

        # 6. Фиксируем изменения в БД
        db.commit()

        # 7. Синхронизирует объект с БД
        db.refresh(new_subscription)

        # 8. Возвращаем данные для обновления UI
        return new_subscription

    except IntegrityError as e:
        print(f"Ошибка целостности БД: {e}")
        return None

    except Exception as e:
        print(f"Ошибка при добавлении подписки: {e}")
        return None


def delete_subscription_from_database(currency_id: int, user_id: int, db: Session):
    """Удаляет подписку пользователя на валюту. Возвращает dict при успехе или None, если не найдена."""

    try:
        # Ищем по составному ключу
        sub = db.get(Subscription, (user_id, currency_id))

        if not sub:
            return None  # Сигнал роуту: "не найдено"

        db.delete(sub)
        db.commit()

        # Возвращаем чистые данные (FastAPI сам упакует их в JSON)
        return {
            "user_id": user_id,
            "currency_id": currency_id
        }

    except Exception as e:
        db.rollback()  # Откат при ошибке БД
        print(f"Ошибка БД: {e}")
        raise RuntimeError("Ошибка сервера при удалении")  # Пробрасываем дальше
