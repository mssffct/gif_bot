import os

from dotenv import load_dotenv

from minio_client import MinioHandler

load_dotenv()

TG_KEY = os.getenv('TELEGRAM_TOKEN')
MINIO_ACCESS = os.getenv('ACCESS_KEY')
MINIO_SECRET = os.getenv('SECRET_KEY')

minio = MinioHandler(MINIO_ACCESS, MINIO_SECRET)
