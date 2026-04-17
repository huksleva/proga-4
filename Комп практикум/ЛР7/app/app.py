import sys
from pathlib import Path
# Находим корень вашего проекта (папку ЛР7)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Вставляем его в САМОЕ НАЧАЛО списка поиска
sys.path.insert(0, str(PROJECT_ROOT))

# Импорт модулей
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from services.s3_service import S3Service
from dotenv import load_dotenv

# Команда для запуска minio.exe
# $env:MINIO_ROOT_USER = "labuser"
# $env:MINIO_ROOT_PASSWORD = "LabPass123!"
# .\minio.exe server data --console-address ":9001"


# Перезагрузка .env
load_dotenv(override=True)

# Настройка Flask с явными путями к шаблонам и статике
template_dir = PROJECT_ROOT / "templates"
static_dir = PROJECT_ROOT / "app" / "static"

app = Flask(
    __name__,
    template_folder=str(template_dir),
    static_folder=str(static_dir),
    static_url_path='/static'
)

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-12345')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Инициализация сервиса
s3_service = S3Service()
s3_service.ensure_bucket_exists()


@app.route('/')
def index():
    """Главная страница со списком файлов"""
    files = s3_service.list_files()
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Загрузка файла"""
    if 'file' not in request.files:
        flash('Файл не найден', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('Файл не выбран', 'error')
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(str(file.filename))
        success, message = s3_service.upload_file(file, filename)

        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')

    return redirect(url_for('index'))


@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    """Удаление файла"""
    success, message = s3_service.delete_file(filename)

    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')

    return redirect(url_for('index'))


@app.route('/presigned/<path:filename>')
def get_presigned_url(filename):
    """Получение presigned URL (API endpoint)"""
    success, result = s3_service.get_presigned_url(filename)

    if success:
        return jsonify({'success': True, 'url': result})
    else:
        return jsonify({'success': False, 'error': str(result)}), 400


@app.route('/download/<path:filename>')
def download_file(filename):
    """Скачивание файла (принудительное, attachment)"""
    try:
        url = s3_service.s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': s3_service.bucket_name,
                'Key': filename,
                'ResponseContentDisposition': f'attachment; filename="{os.path.basename(filename)}"'
            },
            ExpiresIn=3600
        )
        return redirect(url)
    except ClientError as e:
        flash(f'Ошибка при скачивании: {e}', 'error')
        return redirect(url_for('index'))


@app.route('/view/<path:filename>')
def view_file(filename):
    """Просмотр файла в браузере (inline)"""
    try:
        # Получаем Content-Type из метаданных файла
        obj = s3_service.s3_client.head_object(
            Bucket=s3_service.bucket_name,
            Key=filename
        )
        content_type = obj.get('ContentType', 'application/octet-stream')

        url = s3_service.s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': s3_service.bucket_name,
                'Key': filename,
                'ResponseContentType': content_type,
                'ResponseContentDisposition': 'inline'
            },
            ExpiresIn=3600
        )
        return redirect(url)
    except ClientError as e:
        flash(f'Ошибка при просмотре: {e}', 'error')
        return redirect(url_for('index'))


@app.route('/api/files')
def api_list_files():
    """API endpoint для получения списка файлов (JSON)"""
    files = s3_service.list_files()
    return jsonify({'files': files})


if __name__ == '__main__':
    print("Запуск S3 File Manager...")
    app.run(debug=True, host='0.0.0.0', port=5000)


