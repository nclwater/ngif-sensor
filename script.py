import time
import os
import requests
from glob import glob
from datetime import datetime

interval = os.getenv('INTERVAL', 15)
path = os.getenv('DATA_PATH', 'tests/data')
url = os.getenv('UPLOAD_URL', 'test')


def upload_periodically(infinite=True):

    while True:
        for file_path in glob(os.path.join(path, '*(*')):
            print(f'{datetime.now():%Y-%m-%D %H:%M:%S} Uploading {file_path}')
            with open(file_path, 'rb') as f:
                requests.post(url, files={'upload_file': f})
        if not infinite:
            break
        time.sleep(interval*60)


if __name__ == '__main__':
    upload_periodically()
