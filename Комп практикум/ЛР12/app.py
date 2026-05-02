from flask import Flask, jsonify, render_template, request
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

app = Flask(__name__)

# Логин можно задать через переменную окружения, иначе использовать значение по умолчанию
AUTHOR = os.environ.get('MOODLE_LOGIN', '1153307')  # Замените на реальный логин

@app.route('/login', methods=['GET'])
def login():
    """Возвращает авторизационную информацию"""
    return jsonify({"author": AUTHOR})

@app.route('/', methods=['GET'])
def index():
    """Главная страница с описанием лабораторной работы"""
    return render_template('index.html')

@app.route('/api/process-image', methods=['POST'])
def process_image():
    """Пример обработки изображения через Pillow"""
    # Создаем простое изображение для демонстрации работы Pillow
    img = Image.new('RGB', (200, 100), color='lightblue')
    d = ImageDraw.Draw(img)
    d.text((10, 10), "Pillow Demo", fill='black')
    
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