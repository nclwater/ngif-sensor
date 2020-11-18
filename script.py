import time
import os
import requests
from glob import glob


def upload_periodically(infinite=True):
    interval = os.getenv('INTERVAL', 15)
    path = glob(os.path.join(os.getenv('DATA_PATH', 'tests/data'), '*Lysimeter*'))[0]
    url = os.getenv('UPLOAD_URL', 'test')
    while True:
        with open(path, 'rb') as f:
            requests.post(url, files={'upload_file': f})
        if not infinite:
            break
        time.sleep(interval*60)


if __name__ == '__main__':
    upload_periodically()
