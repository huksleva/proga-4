from pymongo import MongoClient
import requests

# подключение к MongoDB
client = MongoClient(
    "mongodb://writer:hahaha@kodaktor.ru:27017/readwriteusers"
)

db = client["readwriteusers"]
collection = db["users"]

# получаем пользователей
users = requests.get(
    "https://fork.kodaktor.ru/getusers1"
).json()

# добавляем записи
for u in users:
    collection.insert_one({
        "login": u["Leonid"],
        "password": u["Tots"]
    })

print("Готово")