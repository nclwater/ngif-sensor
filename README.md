# NGIF Sensor

![Tests](https://github.com/fmcclean/ngif-sensor/workflows/Tests/badge.svg)

Uploads sensor data to the NGIF API

## Usage
`docker run -d -v /home/uo/delta-t:/data --env UPLOAD_URL=http://ngif:5000/upload --env DATA_PATH=/data --name ngif-sensor fmcclean/ngif-sensor` 

## Dependencies
`pip install -r requirements.txt`

## Tests
`python -m unittest`
