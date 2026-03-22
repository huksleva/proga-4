from flask import Flask, request, render_template, send_file, send_from_directory
import os, uuid, io
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ОТКЛЮЧАЕМ сортировку ключей по алфавиту
app.json.sort_keys = False





#================================1-я часть=========================================
@app.route("/login")
def login():
    return {"author": "1153307"}


@app.route("/")
def index():
    # Удаляем временные файлы
    os.chdir(r"./uploads")
    all_files = os.listdir()
    for f in all_files:
        os.remove(f)

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

@app.route("/showPicture_primer", methods=['POST'])
def show_picture_primer():


    file = request.files['image']

    # Проверяем изображение это или нет
    if not is_allowed_image(file):
        return {"result": "invalid filetype"}, 400

    # Обрабатываем изображение
    image = Image.open(file)

    # Сохраняем в память
    # Создаём буфер в памяти (в RAM!)
    buffered = io.BytesIO()

    # Сохраняем изображение в этот буфер
    image.save(buffered, format="PNG")

    # Возвращаем указатель в начало
    buffered.seek(0)

    # Автоматически получаем MIME-тип
    mimetype = Image.MIME.get(image.format, 'application/octet-stream')

    # Отправляем буфер клиенту
    return send_file(buffered, mimetype=mimetype, as_attachment=False, download_name='processed.png')



@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/showPicture', methods=['POST'])
def show_picture():
    file = request.files['image']

    # Проверяем изображение это или нет
    if not is_allowed_image(file):
        return {"result": "invalid filetype"}, 400

    # Сначала сохраняем файл на диск
    original_filename = file.filename.lower()
    ext = original_filename.split('.')[-1] if '.' in original_filename else 'png'
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)  # Сохраняем

    return {"image_url": f"/uploads/{filename}"}









if __name__ == "__main__":
    app.run(debug=True)