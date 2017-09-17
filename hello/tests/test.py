from __future__ import absolute_import

import unittest
import json
from hello.app import create_app
from hello.common.database import db
from fixture import *

class HelloTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_app_serves(self):
        response = self.client.get('/health')
        assert response.status_code == 200

    def test_index_loads(self):
        response = self.client.get('/health')
        assert json.loads(response.data) == {u'Status': u'OK'}

    def test_bad_content_type(self):
        response = self.client.post('/hello/v1/greetings', data=json.dumps({}))
        assert response.status_code == 415

    def test_bad_content(self):
        response = self.client.post('/hello/v1/greetings', data=json.dumps({}), content_type='application/json')
        assert response.status_code == 400

    def test_good_content(self):
        response = self.client.post('/hello/v1/greetings', data=json.dumps(COMPLETE_RECORD), content_type='application/json')
        assert response.status_code == 201

    def test_good_content_retrieve(self):
        response = self.client.post('/hello/v1/greetings', data=json.dumps(COMPLETE_RECORD), content_type='application/json')
        response = self.client.get('/hello/v1/greetings/1', data=json.dumps(COMPLETE_RECORD), content_type='application/json')
        msg = json.loads(response.data)
        assert 'Hey User, have a really nice' in msg['Greeting']

    def test_good_update(self):
        response = self.client.post('/hello/v1/greetings', data=json.dumps(COMPLETE_RECORD), content_type='application/json')
        response = self.client.put('/hello/v1/greetings/1', data=json.dumps(INCOMPLETE_RECORD), content_type='application/json')
        msg = json.loads(response.data)
        assert msg['Status'] == 'updated'

    def test_good_update_retrieve(self):
        response = self.client.post('/hello/v1/greetings', data=json.dumps(COMPLETE_RECORD), content_type='application/json')
        response = self.client.put('/hello/v1/greetings/1', data=json.dumps(INCOMPLETE_RECORD), content_type='application/json')
        response = self.client.get('/hello/v1/greetings/1')
        msg = json.loads(response.data)
        assert 'Hey User, have a very nice' in msg['Greeting']

if __name__ == '__main__':
    unittest.main()
