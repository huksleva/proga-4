from flask import Flask, jsonify, render_template
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    """Возвращает авторизационную информацию"""
    return jsonify({"author": "[ваш_логин_в_moodle]"})

@app.route('/', methods=['GET'])
def index():
    """Главная страница с описанием лабораторной работы"""
    return render_template('index.html')

@app.route('/api/process-image', methods=['POST'])
def process_image():
    """Пример обработки изображения через Pillow"""
    # Здесь можно добавить логику обработки изображений
    return jsonify({"status": "success", "message": "Image processed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)