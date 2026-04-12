from fastapi import Depends, HTTPException, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from starlette.responses import RedirectResponse
from database import *
from schemas import *
from sqlalchemy.orm import Session

app = FastAPI()

# Шаблонизатор
templates = Jinja2Templates(directory="static")

# Монтируем папки
app.mount("/src", StaticFiles(directory="src"), name="src")
app.mount("/css", StaticFiles(directory="css"), name="css")


# GET-запросы

# Главная страница
@app.get("/")
async def main_page():
    return FileResponse("static/index.html")


# Страница с пользователями
@app.get("/users")
async def users_page(request: Request,
                     db: Session = Depends(get_db)):
    # Получаем список пользователей из нашей базы данных
    users = get_users_from_database(db)

    # Отправляем данные в шаблон
    # request обязателен для TemplateResponse
    return templates.TemplateResponse(
        request,
        "users.html",
        {"users": users}
    )


# Страница с курсами валют
@app.get("/currencies")
async def currencies_page(request: Request,
                          db: Session = Depends(get_db)):
    # Получаем курсы валют из нашей базы данных
    currencies = get_currencies_from_database(db)

    # Отправляем данные в шаблон
    # request обязателен для TemplateResponse
    return templates.TemplateResponse(
        request,
        "currencies.html",
        {"currencies": currencies}
    )


# Страница с подписками
@app.get("/subscriptions")
async def subscriptions_page(request: Request,
                             db: Session = Depends(get_db)):
    # Получаем подписки пользователей из нашей базы данных
    subscriptions = get_subscriptions_from_database(db)

    # Отправляем данные в шаблон
    # request обязателен для TemplateResponse
    return templates.TemplateResponse(
        request,
        "subscriptions.html",
        {"subscriptions": subscriptions},
    )


# Страница информации о пользователе
@app.get("/users/{user_id}")
async def users_page(request: Request,
                     user_id: int,
                     db: Session = Depends(get_db)):
    # Получаем данные о пользователе из нашей БД
    user = get_user_from_database(user_id, db)

    # Проверяем существует ли уже такой пользователь
    if not user:
        # Автоматически вызывает обработчик 404
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем курсы валют из нашей базы данных
    currencies = get_currencies_from_database(db)

    # Отправляем данные
    return templates.TemplateResponse(
        request,
        "userinfo.html",
        {"user": user, "currencies": currencies})


# Эндпоинт для ручного обновления списка валют и их курсов
@app.get("/currencies/update")
async def update_currencies_page():
    fill_currency_table()
    return RedirectResponse(url="/currencies")


# POST запросы

# Создаёт нового пользователя
@app.post("/users", response_model=UserResponse)
async def users_page(username: str = Form(...),
                     email: str = Form(...),
                     db: Session = Depends(get_db)):
    user = add_new_user_to_database(username, email, db)
    if not user:
        raise HTTPException(status_code=409, detail="Такой user или email уже существуют, или это другая ошибка в БД")
    return user


# Создаёт новую подписку на валюту для пользователя
@app.post("/subscriptions", response_model=SubscribeResponse)
async def subscriptions_page(user_id: int = Form(...),
                             currency_id: int = Form(...),
                             db: Session = Depends(get_db)):
    sub = add_subscription_to_user(user_id, currency_id, db)
    if not sub:
        raise HTTPException(status_code=409, detail="Пользователь/валюта не найдены или подписка уже существует")
    return sub


# DELETE запросы

# Удаляет пользователя
@app.delete("/users/{user_id}", response_model=DeleteResponse)
async def delete_user(user_id: int,
                      db: Session = Depends(get_db)):
    try:
        # 1. Ищем пользователя
        user = db.get(UserBase, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # 2. Удаляем и коммитим
        db.delete(user)
        db.commit()

        # 3. FastAPI сам сериализует dict в JSON через response_model
        return {"status": "success", "msg": "Пользователь удалён"}

    except HTTPException:
        raise  # Пропускаем наши 404 дальше
    except Exception as e:
        db.rollback()  # Откат при любой ошибке БД
        print(f"Ошибка удаления: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

    return delete_user_from_database(user_id)


# Удаляет подписку пользователя на валюту
@app.delete("/subscriptions", response_model=SubscriptionDeleteResponse)
async def delete_subscription(currency_id: int = Form(...),
                              user_id: int = Form(...),
                              db: Session = Depends(get_db)):
    # 1. Вызываем чистую БД-функцию
    result = delete_subscription_from_database(user_id, currency_id, db)

    # 2. Если вернул None -> подписки нет -> 404
    if result is None:
        raise HTTPException(status_code=404, detail="Подписка не найдена")

    # 3. Иначе -> FastAPI сам проверит результат через response_model и отдаст 200 OK
    return result


# PUT запросы

# Обновляет данные о пользователе по его id
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user_info(user_id: int,
                           username: str = Form(...),
                           email: str = Form(...),
                           db: Session = Depends(get_db)):
    # 1. Вызываем БД-функцию
    result = update_user_from_database(user_id, username, email, db)

    # 2. Если вернул None -> 404
    if result is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # 3. FastAPI сам проверит dict через response_model и отдаст 200 OK
    return result


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
