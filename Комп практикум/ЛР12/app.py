from flask import Flask, jsonify, render_template, request
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
import random
import string

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    """Возвращает авторизационную информацию"""
    return jsonify({"author": 1153307})

@app.route('/', methods=['GET'])
def index():
    """Главная страница с описанием лабораторной работы"""
    return render_template('index.html')

@app.route('/api/process-image', methods=['POST'])
def process_image():
    """Пример обработки изображения через Pillow"""
    # Генерируем случайные параметры
    bg_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    rect_color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    text_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    rect_x1 = random.randint(20, 150)
    rect_y1 = random.randint(20, 100)
    rect_x2 = random.randint(250, 380)
    rect_y2 = random.randint(120, 180)
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # Создаем изображение со случайными параметрами
    img = Image.new('RGB', (400, 200), color=bg_color)
    d = ImageDraw.Draw(img)
    d.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill=rect_color, outline='black', width=2)
    d.text((rect_x1 + 10, rect_y1 + 10), f"Random: {random_text}", fill=text_color, font=None)
    d.text((rect_x1 + 10, rect_y1 + 40), f"Time: {random.randint(1, 24):02d}:{random.randint(0, 59):02d}", fill=text_color, font=None)
    
    # Конвертируем в base64 для отображения в браузере
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return jsonify({
        "status": "success",
        "message": "Image generated with Pillow",
        "image": f"data:image/png;base64,{img_str}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)