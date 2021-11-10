import os
import re
import urllib3
import json
import time

from dotenv import load_dotenv

from minio_client import MinioHandler

load_dotenv()

http = urllib3.PoolManager()
url = 'https://api.telegram.org/'

TG_KEY = os.getenv('TELEGRAM_TOKEN')
MINIO_ACCESS = os.getenv('ACCESS_KEY')
MINIO_SECRET = os.getenv('SECRET_KEY')

minio = MinioHandler(MINIO_ACCESS, MINIO_SECRET)


class LongPolling:
    def __init__(self, bot_name, token):
        self.bot_name = bot_name
        self.token = token
        self.response = url + self.bot_name + self.token + '/getUpdates'
        self.get_updates()

    def get_updates(self):
        while True:
            time.sleep(1)
            return http.request('GET', self.response)
