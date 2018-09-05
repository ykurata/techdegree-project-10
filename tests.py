import os
import datetime
import unittest
import tempfile

from app import app
from models import User, Todo


class AppTest(unittest.TestCase):
    """ Set up and tear down"""
    def setUp(self):
        self.db, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db)
        os.unlink(app.config['DATABASE'])

    def test_my_todos_status_code(self):
        """Test my_todos returns status code 200"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_todos(self):
        """Test api returns 200 status code"""
        response = self.app.get('/api/v1/todos')
        self.assertEqual(response.status_code, 200)

    def test_get_single_todo(self):
        """Test api returns status code 404 if there is no specific todo"""
        response = self.app.get('/api/v1/todos/1')
        self.assertEqual(response.status_code, 404)

    def test_delete_todo(self):
        """Test api returns status code 204 when delete method is called"""
        response = self.app.delete('/api/v1/todos/1')
        self.assertEqual(response.status_code, 204)

    def test_post_user(self):
        """Test api returns status code 400 when there is no user"""
        response = self.app.post('/api/v1/users')
        self.assertEqual(response.status_code, 400)


    def create_user(self, username, email, password, verify_password):
        return self.app.post(
            '/api/v1/users',
            data=dict(
                username=username,
                email=email,
                password=password,
                verify_password=verify_password))


    def test_valid_user_registration(self):
        response = self.create_user(
            'test user',
            'email@example.com',
            'password',
            'password2')
        self.assertIn(b'Password and password verification do not match',
                        response.data)


if __name__ == '__main__':
    unittest.main()
