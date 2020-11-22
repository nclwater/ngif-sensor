import unittest
import script
from pymongo import MongoClient

db = MongoClient('mongodb://test:password@localhost:27017/').test

db.readings.drop()
db.sensors.drop()


class TestScript(unittest.TestCase):
    def test(self, ):
        script.upload_periodically(infinite=False)
