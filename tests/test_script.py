import unittest
import script
from unittest import mock


def mocked_requests_post(*args, **kwargs):
    assert 'upload_file' in kwargs['files']


class TestScript(unittest.TestCase):

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test(self, mock_post):
        script.upload_periodically(infinite=False, read=True, remove=False)
