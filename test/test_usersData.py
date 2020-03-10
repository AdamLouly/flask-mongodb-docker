import unittest
import os
from app import app
import json
from config import client

class BasicTests(unittest.TestCase):
     
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_get_initial_response(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        user = {
            "username":"test",
            "password":"testpass"
        }
        response = self.app.post('/api/v1/create',data = json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.app.post('/api/v1/create',content_type='application/json')
        self.assertEqual(response.status_code, 400)

 
if __name__ == "__main__":
    unittest.main()