import unittest
import json
from api import app, db, userTable, messageTable, tagsTable, messageTagsTable

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        userTable.insert({
            "name": "testname",
            "email": "testmail@mail.com"
        })

        messageTable.insert({
            "message": "test message",
            "userId": "1"
        })
        tagsTable.insert({
            "tag": "testtag"
        })

        messageTagsTable.insert({
            "tag_id": "1",
            "message_id": "1"
        })     

    def tearDown(self):
        db['users'].drop() 
        db['messages'].drop()
        db['tags'].drop()
        db['messageTags'].drop()

    def test_create_user(self):
        response = self.app.post('/create-user', json={"name": "Testname", "email": "test@example.com"})
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertIn("userId", data)

    def test_get_user(self):
        response = self.app.get('/get-user/1')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn("name", data) 

if __name__ == '__main__':
    unittest.main()
