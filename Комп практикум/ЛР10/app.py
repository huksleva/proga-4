import os
import io
from flask import Flask, request, jsonify, render_template, send_file
from PIL import Image
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

app = Flask(__name__)

# 1. Проверка наличия токена
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("Ошибка: Переменная окружения HF_TOKEN не найдена в файле .env")

# 2. Инициализация клиента с тайм-аутом 30 секунд
client = InferenceClient(token=HF_TOKEN, timeout=30)


@app.route('/login', methods=['GET'])
def login():
    """Маршрут /login: возвращает JSON с логином автора"""
    return jsonify({"author": "1153307"})


@app.route('/makeimage', methods=['GET'])
def makeimage_get():
    """Маршрут GET /makeimage: возвращает HTML-форму"""
    return render_template('makeimage.html', message=None)


@app.route('/makeimage', methods=['POST'])
def makeimage_post():
    """Маршрут POST /makeimage: валидация, генерация и возврат JPEG"""
    # Сохраняем данные формы для повторного отображения при ошибке
    form_data = {
        'width': request.form.get('width', ''),
        'height': request.form.get('height', ''),
        'text': request.form.get('text', '')
    }

    # --- ВАЛИДАЦИЯ ---
    try:
        w = int(form_data['width'])
        h = int(form_data['height'])
    except (ValueError, TypeError):
        return render_template('makeimage.html', message="Invalid image size", **form_data)

    if w <= 0 or h <= 0:
        return render_template('makeimage.html', message="Invalid image size", **form_data)

    if w % 32 != 0 or h % 32 != 0:
        return render_template('makeimage.html', message="Width and height must be multiples of 32", **form_data)

    # Опциональное ограничение диапазона (рекомендовано в задании)
    if not (256 <= w <= 1024) or not (256 <= h <= 1024):
        return render_template('makeimage.html', message="Invalid image size", **form_data)

    prompt = form_data['text'].strip()
    if not prompt:
        return render_template('makeimage.html', message="Prompt cannot be empty", **form_data)

    # --- ГЕНЕРАЦИЯ И ОБРАБОТКА ---
    try:
        # Вызов модели. Передаем параметры напрямую.
        # InferenceClient.text_to_image возвращает объект PIL.Image
        img = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell",
            width=w,
            height=h
        )

        # Согласно заданию: открываем через io.BytesIO
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        image = Image.open(buffer)

        # Конвертируем в RGB (на случай, если модель вернула RGBA или grayscale)
        image = image.convert("RGB")

        # Если модель проигнорировала размеры, ресайзим принудительно
        if image.size != (w, h):
            image = image.resize((w, h), Image.Resampling.LANCZOS)

        # Сохраняем в JPEG с качеством 90
        jpeg_buffer = io.BytesIO()
        image.save(jpeg_buffer, format="JPEG", quality=90)
        jpeg_buffer.seek(0)

        # Возвращаем HTTP-ответ с заголовком image/jpeg
        return send_file(jpeg_buffer, mimetype="image/jpeg")

    except Exception as e:
        # Обработка тайм-аутов, квот, сетевых ошибок и ошибок модели
        error_msg = str(e)
        return render_template('makeimage.html', message=f"Model generation failed: {error_msg}", **form_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)