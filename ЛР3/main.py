from fastapi import FastAPI
from database import create_db_and_tables, add_all_currency_valute
# from sqlalchemy.orm import sessionmaker
# from contextlib import asynccontextmanager



app = FastAPI()


@app.get("/")
def mainPage():
    pass

























if __name__ == "__main__":
    # Создание всех таблиц
    create_db_and_tables()

    # Заполняем таблицу с валютами
    add_all_currency_valute()




