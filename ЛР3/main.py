from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse
import os
from pathlib import Path
from database import (
    create_db_and_tables,
    fill_currency_table,
    drop_db_and_tables,
    get_currencies_from_database,
    get_users_from_database,
    get_subscriptions_from_database,
    add_new_user_to_database)


app = FastAPI()

# Шаблонизатор
templates = Jinja2Templates(directory="static")


# GET-запросы

# Главная страница
@app.get("/")
def main_page():
    return FileResponse("static/index.html")

# Страница с пользователями
@app.get("/users")
def users_page(request: Request):
    # Получаем список пользователей из нашей базы данных
    users = get_users_from_database()

    # Отправляем данные в шаблон
    # request обязателен для TemplateResponse
    return templates.TemplateResponse(
        request,
        "users.html",
        {"users": users}
    )

# Страница с курсами валют
@app.get("/currencies")
def currencies_page(request: Request):
    # Получаем курсы валют из нашей базы данных
    currencies = get_currencies_from_database()

    # Отправляем данные в шаблон
    # request обязателен для TemplateResponse
    return templates.TemplateResponse(
        request,
        "currencies.html",
        {"currencies": currencies},
    )

# Страница с подписками
@app.get("/subscriptions")
def subscriptions_page(request: Request):
    # Получаем подписки пользователей из нашей базы данных
    subscriptions = get_subscriptions_from_database()

    # Отправляем данные в шаблон
    # request обязателен для TemplateResponse
    return templates.TemplateResponse(
        request,
        "subscriptions.html",
        {"subscriptions": subscriptions},
    )



# POST запросы

# Создаёт нового пользователя
@app.post("/users")
def users_page(username: str = Form(...), email: str = Form(...)):
    add_new_user_to_database(username, email)
    return RedirectResponse("/users", status_code=303)





# DELETE запросы

# Удаляет нового пользователя


# Создать нового пользователя (принимает username и email)


















if __name__ == "__main__":

    # Удаляем все таблицы
    drop_db_and_tables()

    # Создание всех таблиц
    create_db_and_tables()

    # Заполняем таблицу с валютами
    fill_currency_table()

    # Запускаем сервер
    os.system("uvicorn main:app --reload")
