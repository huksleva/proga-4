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
def get_currency_valute():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    root = etree.fromstring(response.content)
    return root


# Заполняем таблицу с валютами
def add_all_currency_valute():
    root = get_currency_valute()
    try:


        # Работает с неймспейсами: ищет элементы по локальному имени
        for el in root.xpath("//Valute"):
            name_el = el.find("Name")
            id_el = el.find("ID")
            code_el = el.find("CharCode")



            # Пропускаем, если нет обязательных полей
            if any(x is None or x.text is None for x in [name_el, id_el, code_el]):
                    continue

            # Формируем ответ
            record = Currency(
                id=id_el.text,
                code=code_el.text,
                name=name_el.text
            )

            Session().add(record)
            print(record)

        Session().commit()

    except Exception as e:
        print(f"Ошибка: {e}")
        Session().rollback()

add_all_currency_valute()


def debug_xpath(root, xpath_expr, description=""):
    """Помогает понять, почему XPath не работает"""
    print(f"\n🔍 Проверка: {description or xpath_expr}")

    # 1. Проверяем синтаксис
    try:
        result = root.xpath(xpath_expr)
    except etree.XPathEvalError as e:
        print(f"  ❌ Синтаксическая ошибка: {e}")
        return False

    # 2. Проверяем результат
    if not result:
        print(f"  ⚠️ Ничего не найдено (возможно, проблема с неймспейсом)")
        # Попробуем без неймспейса
        alt = xpath_expr.replace("ns:", "").replace("{http://web.cbr.ru/}", "")
        if alt != xpath_expr:
            alt_result = root.xpath(alt)
            if alt_result:
                print(f"  ✓ Нашлось без неймспейса: {len(alt_result)} элементов")
        return False

    print(f"  ✓ Найдено: {len(result)} элементов")
    return True


# Использование:
debug_xpath(root, "//Valute", "Поиск валют")
debug_xpath(root, "//ns:Valute", "Поиск с неймспейсом", )
debug_xpath(root, "//*[local-name()='Valute']", "Поиск по local-name()")
