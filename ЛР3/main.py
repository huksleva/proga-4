from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse
import os
from database import (
    create_db_and_tables,
    add_all_currency_valute,
    drop_db_and_tables,
    get_valute)


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
def users_page():
    return FileResponse("static/users.html")

# Страница с курсами валют
@app.get("/currencies")
def currencies_page(request: Request):
    currencies = get_valute()

    # Отправляем данные в шаблон
    # request обязателен для TemplateResponse
    return templates.TemplateResponse(
        request,
        "currencies.html",
        {"currencies": currencies},
    )

# Страница с курсами валют
@app.get("/subscriptions")
def subscriptions_page():
    return FileResponse("static/subscriptions.html")



# POST запросы

@app.post("/users")
def users_page(username: str = Form(...), email: str = Form(...)):
    print(username, email)
    return RedirectResponse("/users", status_code=303)





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
