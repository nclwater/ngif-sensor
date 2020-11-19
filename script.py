import time
import os
import requests
import subprocess

interval = os.getenv('INTERVAL', 15)
path = os.getenv('DATA_PATH', 'tests/data')
url = os.getenv('UPLOAD_URL', 'test')


def upload_periodically(infinite=True, read=True, remove=True):

    while True:
        if remove:
            for file_path in os.listdir(path):
                os.remove(os.path.join(path, file_path))
        if read:
            read_from_sensor()
        for file_path in os.listdir(path):
            with open(os.path.join(path, file_path), 'rb') as f:
                requests.post(url, files={'upload_file': f})
        if not infinite:
            break
        time.sleep(interval*60)


def read_from_sensor():
    subprocess.call(r"wineconsole cmd / c 'Z:\home\uo\wine\DL4CmdLine COM99 /DZ:\home\uo\ngif-sensor\data'")


if __name__ == '__main__':
    upload_periodically()
