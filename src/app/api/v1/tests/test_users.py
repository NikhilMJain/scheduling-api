from sqlite3 import IntegrityError

from src.app.api.v1.tests.base_test_case import BaseTestCase


class TestUsers(BaseTestCase):
    def test_create_user(self):
        payload = dict(first_name='Nikhil', last_name='Jain', email='nik@gmail.com')
        response = self.client.post("/v1/users/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()), 3)

    def test_already_existing_email(self):
        payload = dict(first_name='Nikhil', last_name='Jain', email='nik@gmail.com')
        self.client.post("/v1/users/", json=payload)
        self.assertRaises(IntegrityError, self.client.post, "/v1/users/", json=payload)

    def test_get_user(self):
        payload = dict(first_name='Nikhil', last_name='Jain', email='nik@gmail.com')
        response = self.client.post("/v1/users/", json=payload)
        user_id = response.headers.get('location').split('/')[-1]
        token = response.json().get('token')
        response = self.client.get('/v1/users/{}'.format(user_id), headers=dict(Authorization='Bearer {}'.format(
            token)))
        self.assertEqual(response.status_code, 200)
