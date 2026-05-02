FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей для Pillow (опционально)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Порт для Flask-приложения
EXPOSE 8080

# Переменная окружения для логина (можно переопределить при запуске)
ENV MOODLE_LOGIN=leonid_ivanov

# Запуск через gunicorn для продакшена
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]