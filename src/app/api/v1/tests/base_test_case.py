import os
import random
from unittest import TestCase

from src.app.api.v1.tests.conftest import client


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.client = client()

    def tearDown(self) -> None:
        os.remove('sqlite.db')

    def get_auth_header(self):
        user_payload = dict(first_name='Nikhil', last_name='Jain', email='nik@gmail{}.com'.format(random.randint(0,
                                                                                                                 100)))
        response = self.client.post("/v1/users/", json=user_payload)
        return dict(Authorization='Bearer {}'.format(response.json()['token']),
                    user_id=response.headers.get('location').split('/')[-1])
