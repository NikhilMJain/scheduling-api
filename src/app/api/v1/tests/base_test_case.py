import os
from unittest import TestCase

from src.app.api.v1.tests.conftest import client


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.client = client()

    def tearDown(self) -> None:
        os.remove('sqlite.db')