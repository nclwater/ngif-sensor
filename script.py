import time
import os
import requests
import subprocess
from glob import glob

interval = os.getenv('INTERVAL', 15)
path = os.getenv('DATA_PATH', 'tests/data')
url = os.getenv('UPLOAD_URL', 'test')
sensor_ports = os.getenv('SENSOR_PORTS', '').split()


def upload_periodically(infinite=True):

    while True:
        for file_path in glob(os.path.join(path, '*(*')):
            with open(file_path, 'rb') as f:
                requests.post(url, files={'upload_file': f})
        if not infinite:
            break
        time.sleep(interval*60)


if __name__ == '__main__':
    upload_periodically()
