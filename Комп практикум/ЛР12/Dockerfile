FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Порт для Flask-приложения
EXPOSE 8080

# Запуск через gunicorn для продакшена
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]