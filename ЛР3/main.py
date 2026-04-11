from fastapi import HTTPException
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from starlette.responses import RedirectResponse

from database import *


app = FastAPI()

# Шаблонизатор
templates = Jinja2Templates(directory="static")

# Монтируем папки
app.mount("/src", StaticFiles(directory="src"), name="src")
app.mount("/css", StaticFiles(directory="css"), name="css")




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
        {"currencies": currencies}
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

# Страница информации о пользователе
@app.get("/users/{user_id}")
def users_page(request: Request, user_id: int):
    # Получаем данные о пользователе из нашей БД
    user = get_user_from_database(user_id)

    # Проверяем существует ли уже такой пользователь
    if not user:
        # Автоматически вызывает обработчик 404
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем курсы валют из нашей базы данных
    currencies = get_currencies_from_database()

    # Отправляем данные
    return templates.TemplateResponse(
    request,
    "userinfo.html",
    {"user": user, "currencies": currencies})

# Эндпоинт для ручного обновления списка валют и их курсов
@app.get("/currencies/update")
def update_currencies_page():
    fill_currency_table()
    return RedirectResponse(url="/currencies")




# POST запросы

# Создаёт нового пользователя
@app.post("/users")
def users_page(username: str = Form(...), email: str = Form(...)):
    json_response = add_new_user_to_database(username, email)
    return json_response

# Создаёт новую подписку на валюту для пользователя
@app.post("/subscriptions")
def subscriptions_page(user_id: int = Form(...), currency_id: int = Form(...)):
    return add_subscription_to_user(user_id, currency_id)




# DELETE запросы

# Удаляет пользователя
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return delete_user_from_database(user_id)

# Удаляет подписку пользователя на валюту
@app.delete("/subscriptions")
def delete_subscription(currency_id: int = Form(...), user_id: int = Form(...)):
    return delete_subscription_from_database(currency_id, user_id)




# PUT запросы

# Обновляет данные о пользователе по его id
@app.put("/users/{user_id}")
def update_user_info(user_id: int, username: str = Form(...), email: str = Form(...)):
    return update_user_from_database(user_id, username, email)




# Обработчик 404
@app.exception_handler(404)
async def custom_404(request: Request, exc):
    return templates.TemplateResponse(
        request,
        "404.html",
        status_code=404
    )










if __name__ == "__main__":

    # Удаляем все таблицы
    drop_db_and_tables()

    # Создание всех таблиц
    create_db_and_tables()

    # Заполняем таблицу с валютами
    fill_currency_table()

    # Запускаем сервер
    os.system("uvicorn main:app --reload")
