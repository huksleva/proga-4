from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from ser import S3Service
import os
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.mount("/static", StaticFiles(directory="static"), name="static")

s3_service = S3Service()

# Инициализация бакета при запуске
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
    """Получение presigned URL"""
    success, result = s3_service.get_presigned_url(filename)

    if success:
        return jsonify({'success': True, 'url': result})
    else:
        return jsonify({'success': False, 'error': result}), 400


@app.route('/download/<path:filename>')
def download_file(filename):
    """Скачивание файла через presigned URL (редирект)"""
    success, url = s3_service.get_presigned_url(filename, expiration=3600)

    if success:
        return redirect(url)
    else:
        flash('Ошибка при получении ссылки для скачивания', 'error')
        return redirect(url_for('index'))


@app.route('/view/<path:filename>')
def view_file(filename):
    """Просмотр файла (для изображений, текстовых файлов)"""
    success, content, content_type = s3_service.get_file_content(filename)

    if success:
        return send_file(
            BytesIO(content),
            mimetype=content_type,
            as_attachment=False
        )
    else:
        flash('Ошибка при получении файла', 'error')
        return redirect(url_for('index'))


@app.route('/api/files')
def api_list_files():
    """API endpoint для получения списка файлов"""
    files = s3_service.list_files()
    return jsonify({'files': files})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)













