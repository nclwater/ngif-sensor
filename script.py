import time
import os
import pandas as pd
from glob import glob
from datetime import datetime
from pymongo import MongoClient,  DESCENDING

interval = os.getenv('INTERVAL', 15)
path = os.getenv('DATA_PATH', 'tests/data')
mongo_uri = os.getenv('MONGO_URI', 'mongodb://test:password@localhost:27017/test?authSource=admin')

db = MongoClient(mongo_uri).get_database()
readings = db.readings
sensors = db.sensors


def upload_periodically(infinite=True, tolerant=True):

    while True:
        for file_path in glob(os.path.join(path, '*(*')):
            log(f'Uploading {file_path}')
            try:
                upload_file(file_path)
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


def upload_file(file_path):
    name = os.path.basename(file_path)
    name = name[11:-25]

    with open(file_path) as f:
        # Update sensors collection
        sensors.update_one({'name': name}, {'$set': {field.replace('.', '-'): unit for field, unit in zip(
                f.readline().strip().split('\t'), f.readline().strip().split('\t'))}
        }, upsert=True)

    data = pd.read_csv(file_path, sep='\t', parse_dates=[0], dayfirst=True, skiprows=range(1, 2), na_values=['#+INF'])
    data = data.rename(columns={**{data.columns[0]: 'time'},
                                **{field: field.replace('.', '-') for field in data.columns if '.' in field}})
    # Get the latest inserted time
    last_entry = readings.find_one(
        {'name': name}, {'time': 1},
        sort=[('_id', DESCENDING)]
    )
    if last_entry is not None:
        last_time = pd.to_datetime(last_entry['time'])
        data = data[data.time > last_time]

    if len(data) > 0:
        readings.insert_many({'name': name, **{k: v for k, v in row.items() if pd.notna(v)}}
                             for row in data.to_dict('records'))


if __name__ == '__main__':
    upload_periodically()
