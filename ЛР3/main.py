from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from database import create_db_and_tables, add_all_currency_valute, drop_db_and_tables


app = FastAPI()

# Главная страница
@app.get("/")
def main_page():
    return FileResponse("static/index.html")

# Страница с пользователями
@app.get("/users")
def users_page():
    return FileResponse("static/users.html")

# Страница с курсами валют
@app.get("/currencies")
def currencies_page():
    return FileResponse("static/currencies.html")

# Страница с курсами валют
@app.get("/subscriptions")
def subscriptions_page():
    return FileResponse("static/subscriptions.html")









# Создать нового пользователя (принимает username и email)


















if __name__ == "__main__":

    # Удаляем все таблицы
    drop_db_and_tables()

    # Создание всех таблиц
    create_db_and_tables()

    # Заполняем таблицу с валютами
    add_all_currency_valute()

    # Запускаем сервер
    os.system("uvicorn main:app --reload")
