import time
import os
import requests


def upload_periodically(infinite=True):
    interval = os.getenv('INTERVAL', 15)
    path = os.getenv('DATA_PATH', 'tests/data.csv')
    url = os.getenv('UPLOAD_URL', 'test')
    while True:
        with open(path, 'rb') as f:
            requests.post(url, files={'upload_file': f})
        if not infinite:
            break
        time.sleep(interval*60)
