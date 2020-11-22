import time
import os
import pandas as pd
from glob import glob
from datetime import datetime
from pymongo import MongoClient,  DESCENDING

interval = os.getenv('INTERVAL', 15)
data_path = os.getenv('DATA_PATH', 'tests/data')
mongo_uri = os.getenv('MONGO_URI', 'mongodb://test:password@localhost:27017/test?authSource=admin')

db = MongoClient(mongo_uri).get_database()
readings = db.readings
sensors = db.sensors


class File:
    def __init__(self, name: str, data: pd.DataFrame, units: dict, path: str):
        self.name = name
        self.data = data
        self.units = units
        self.path = path

    def upload(self):
        sensors.update_one({'name': self.name}, {'$set': self.units}, upsert=True)

        # Get the latest inserted time
        last_entry = readings.find_one(
            {'name': self.name}, {'time': 1},
            sort=[('_id', DESCENDING)]
        )
        if last_entry is not None:
            last_time = pd.to_datetime(last_entry['time'])
            self.data = self.data[self.data.time > last_time]

        if len(self.data) > 0:
            # Insert in sets of 1000
            for chunk in chunks(self.data.to_dict('records'), 1000):
                readings.insert_many({'name': self.name, **{k: v for k, v in row.items() if pd.notna(v)}}
                                     for row in chunk)


def upload_periodically(infinite=True, tolerant=True):

    while True:
        files = []
        for file_path in glob(os.path.join(data_path, '*(*')):
            files.append(read_file(file_path))
        for file in files:
            log(f'Uploading {file.path}')
            try:
                file.upload()
                log('Done')
            except Exception as e:
                if tolerant:
                    log(f"Upload failed ({e})'")
                else:
                    raise e
        if not infinite:
            break
        time.sleep(interval*60)


def log(s):
    print(f'{datetime.now():%Y-%m-%D %H:%M:%S} {s}')


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def read_file(file_path):
    name = os.path.basename(file_path)
    name = name[:-25]

    with open(file_path) as f:
        # Read units
        units = {field.replace('.', '-'): unit for field, unit in zip(
            f.readline().strip().split('\t'), f.readline().strip().split('\t'))}

    data = pd.read_csv(file_path, sep='\t', parse_dates=[0], dayfirst=True, skiprows=range(1, 2), na_values=['#+INF'])
    data = data.rename(columns={**{data.columns[0]: 'time'},
                                **{field: field.replace('.', '-') for field in data.columns if '.' in field}})
    return File(name, data, units, file_path)


if __name__ == '__main__':
    upload_periodically()
