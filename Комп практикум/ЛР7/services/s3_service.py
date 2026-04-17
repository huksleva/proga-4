import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import mimetypes

load_dotenv()


class S3Service:
    def __init__(self):
        self.endpoint_url = os.getenv('AWS_ENDPOINT_URL', 'http://localhost:9000')
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region = os.getenv('AWS_REGION', 'ru-central1')
        self.bucket_name = os.getenv('BUCKET_NAME', 'my-bucket')

        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'}
            )
        )

    def ensure_bucket_exists(self):
        """Создает бакет, если он не существует"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Бакет {self.bucket_name} создан")

    def list_files(self):
        """Получить список всех файлов в бакете"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                files = []
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified']
                    })
                return files
            return []
        except ClientError as e:
            print(f"Ошибка при получении списка файлов: {e}")
            return []

    def upload_file(self, file_object, filename):
        content_type, _ = mimetypes.guess_type(filename)
        try:
            self.s3_client.upload_fileobj(
                file_object,
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': content_type or 'application/octet-stream'}
            )
            return True, f"Файл {filename} успешно загружен"
        except ClientError as e:
            return False, f"Ошибка при загрузке файла: {e}"

    def delete_file(self, filename):
        """Удалить файл из бакета"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            return True, f"Файл {filename} успешно удален"
        except ClientError as e:
            return False, f"Ошибка при удалении файла: {e}"

    def get_presigned_url(self, filename, expiration=3600):
        """Получить presigned URL для файла"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': filename
                },
                ExpiresIn=expiration
            )
            return True, url
        except ClientError as e:
            return False, f"Ошибка при создании presigned URL: {e}"

    def get_file_content(self, filename):
        """Получить содержимое файла"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            return True, response['Body'].read(), response['ContentType']
        except ClientError as e:
            return False, None, f"Ошибка при получении файла: {e}"