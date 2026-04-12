from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from datetime import datetime
from models import Base, Currency, UserBase, Subscription
import requests
from lxml import etree

# Ссылки
cbr_url = "https://www.cbr.ru/scripts/XML_daily.asp"
DATABASE_URL = "sqlite+aiosqlite:///./db/database.db"

# Создание движка
engine = create_async_engine(DATABASE_URL, echo=False)

# Фабрика асинхронных сессий
# expire_on_commit=False важно для async, чтобы объекты не "отваливались" после commit
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """Функция-генератор зависимости"""

    async with async_session_factory() as session:
        yield session


async def create_db_and_tables():
    """Создание всех таблиц"""

    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Ошибка: {e}")


async def drop_db_and_tables():
    """Удаление всех таблиц"""

    try:
        Base.metadata.drop_all(engine)
    except Exception as e:
        print(f"Ошибка: {e}")


async def get_currencies_cbr():
    """Получаем курсы валют в формате xml от ЦБ РФ"""

    response = requests.get(cbr_url)
    root = etree.fromstring(response.content)
    return root


async def fill_currency_table():
    """Заполняем таблицу с валютами"""

    valute = get_currencies_cbr().xpath("//Valute")

    try:
        async with async_session_factory() as session:
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
            await session.commit()

    except Exception as e:
        print(f"Ошибка: {e}")
        await session.rollback()


async def get_currencies_from_database(db: AsyncSession):
    """Возвращает базу данных курсов валют"""

    result = await db.execute(select(Currency))
    currencies = result.scalars().all()
    return currencies


async def get_users_from_database(db: AsyncSession):
    """Возвращает базу данных пользователей"""

    result = await db.execute(select(UserBase))
    users = result.scalars().all()
    return users


async def get_user_from_database(user_id: int, db: AsyncSession):
    """Возвращает информацию о пользователе по его id"""

    user = db.get(UserBase, user_id)
    return user


async def get_subscriptions_from_database(db: AsyncSession):
    """Возвращает базу данных подписок пользователей"""

    result = await db.execute(select(Subscription))
    subscriptions = result.scalars().all()
    return subscriptions


async def add_new_user_to_database(user_name: str, e_mail: str, db: AsyncSession):
    """Добавляет нового пользователя в базу данных. Ответ возвращает в формате JSON."""

    try:
        # Проверяем (email и username должны быть уникальны у каждого пользователя)
        # Проверяем имя
        result = await db.execute(select(UserBase).where(UserBase.username == user_name))
        if result.scalars().first():
            return None

        # Проверяем почту
        result = await db.execute(select(UserBase).where(UserBase.email == e_mail))
        if result.scalars().first():
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
        await db.commit()

        # 4. Важно, чтобы получить id после commit
        await db.refresh(new_user)

        # 5. Отправляем ответ
        return new_user

    except Exception as e:
        print(f"Критическая ошибка БД: {e}")
        return None


async def update_user_from_database(user_id: int, new_username: str, new_email: str, db: AsyncSession):
    """Обновляет данные пользователя в БД"""

    try:
        updatetable_user = await db.get(UserBase, user_id)

        if not updatetable_user:
            return None  # Сигнал роуту: пользователь не найден

        # Обновляем данные
        updatetable_user.username = new_username
        updatetable_user.email = new_email

        await db.commit()
        await db.refresh(updatetable_user)  # Синхронизируем объект с БД после коммита

        return updatetable_user

    except Exception as e:
        await db.rollback()
        print(f"Ошибка обновления: {e}")
        raise RuntimeError("Ошибка сервера при обновлении")


async def add_subscription_to_user(user_id: int, currency_id: int, db: AsyncSession):
    """Создаёт новую подписку на валюту для пользователя. Нужен id пользователя и id валюты"""

    try:
        # 1. Проверяем, существует ли пользователь
        if not await db.get(UserBase, user_id):
            return None

        # 2. Проверяем, существует ли валюта
        if not await db.get(Currency, currency_id):
            return None

        # 3. Проверяем, нет ли уже такой подписки. Проверяем по уникальному ключу
        if await db.get(Subscription, (user_id, currency_id)):
            return None

        # 4. Создаём новую подписку
        new_subscription = Subscription(
            user_id=user_id,
            currency_id=currency_id
        )

        # 5. Добавляем в сессию (готовим к отправке)
        db.add(new_subscription)

        # 6. Фиксируем изменения в БД
        await db.commit()

        # 7. Синхронизирует объект с БД
        await db.refresh(new_subscription)

        # 8. Возвращаем данные для обновления UI
        return new_subscription

    except IntegrityError as e:
        print(f"Ошибка целостности БД: {e}")
        return None

    except Exception as e:
        print(f"Ошибка при добавлении подписки: {e}")
        return None


async def delete_subscription_from_database(currency_id: int, user_id: int, db: AsyncSession):
    """Удаляет подписку пользователя на валюту. Возвращает dict при успехе или None, если не найдена."""

    try:
        # Ищем по составному ключу
        sub = await db.get(Subscription, (user_id, currency_id))

        if not sub:
            return None  # Сигнал роуту: "не найдено"

        await db.delete(sub)
        await db.commit()

        # Возвращаем чистые данные (FastAPI сам упакует их в JSON)
        return {
            "user_id": user_id,
            "currency_id": currency_id
        }

    except Exception as e:
        await db.rollback()  # Откат при ошибке БД
        print(f"Ошибка БД: {e}")
        raise RuntimeError("Ошибка сервера при удалении")  # Пробрасываем дальше
