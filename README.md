# NGIF Sensor

![Tests](https://github.com/fmcclean/ngif-sensor/workflows/Tests/badge.svg)

Uploads sensor data to the NGIF API

## Usage
`docker run -d -v /home/uo/delta-t:/data --env MONGO_URI=mongodb://user:password@hostname:27017/database?authSource=admin --env DATA_PATH=/data --restart unless-stopped --name ngif-sensor fmcclean/ngif-sensor ` 

## Dependencies
`pip install -r requirements.txt`

## Tests
`python -m unittest`
