from flask import Flask, request, render_template, send_from_directory
import os, uuid
from PIL import Image
import json


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.secret_key = 'dev_key_123'


# ОТКЛЮЧАЕМ сортировку ключей по алфавиту
app.json.sort_keys = False


STATE_FILE = 'last_upload.json'

# Загрузка состояния при запуске
def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

# Сохранение состояния
def save_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)

# Загружаем состояние при старте
app_state = load_state()







#================================1-я часть=========================================
@app.route("/login")
def login():
    return {"author": "1153307"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/size2json", methods=['POST'])
def size_to_json():
    img = request.files['image']
    image = Image.open(img.stream)

    # Проверка на .png
    if image.format != "PNG":
        return {"result": "invalid filetype"}

    return {"width": image.size[0], "height": image.size[1]}
#==================================================================================







#================================2-я часть=========================================
PIL_FORMATS = [
    'PNG', 'JPEG', 'JPG', 'GIF', 'BMP', 'WEBP', 'ICO',
    'TIFF', 'TIF', 'PSD', 'RAW', 'CR2', 'NEF', 'ARW',
    'DNG', 'EPS', 'PDF', 'PPM', 'PGM', 'PBM', 'XBM',
    'XPM', 'SGI', 'SUN', 'TGA', 'PCX', 'PICT', 'SPIDER',
    'FITS', 'FLI', 'FLC', 'FTEX', 'GBR', 'GIMP', 'HDF5',
    'MCIDAS', 'MIC', 'MPO', 'MSP', 'PALM', 'PCD', 'PIXAR',
    'QOI', 'WAL', 'WMF', 'EMF', 'DCX', 'IM'
]

# Проверка на изображение
def is_allowed_image(file):
    from PIL import Image, UnidentifiedImageError

    try:
        img = Image.open(file.stream)
        img.verify()
        file.stream.seek(0)
        img = Image.open(file.stream)

        return img.format in PIL_FORMATS
    except (UnidentifiedImageError, IOError, OSError):
        return False

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/showPicture', methods=['POST'])
def show_picture():
    file = request.files['image']

    # Проверяем изображение это или нет
    if not is_allowed_image(file):
        return {"result": "invalid filetype"}, 400

    # Сбрасываем позицию потока в начало
    file.stream.seek(0)

    # Сначала сохраняем файл на диск
    original_filename = file.filename.lower()
    ext = original_filename.split('.')[-1] if '.' in original_filename else 'png'
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)  # Сохраняем

    # Сохраняем в файл
    global app_state
    app_state = {
        'image_url': f"/uploads/{filename}",
        'filename': filename,
        'ext': ext
    }
    save_state(app_state)

    return {"image_url": f"/uploads/{filename}"}


# Возвращает данные о последнем загруженном файле
@app.route('/lastUpload')
def last_upload():
    global app_state
    if app_state:
        return app_state
    return {"result": "no uploads yet"}, 404


# Маршрут для очистки папки uploads
@app.route('/clearUploads', methods=['POST'])
def clear_uploads():
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        return {"result": "uploads cleared"}
    except Exception as e:
        return {"error": str(e)}, 500
#==================================================================================



if __name__ == "__main__":
    app.run(debug=True)