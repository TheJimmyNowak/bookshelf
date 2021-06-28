from app import create_app
from unittest import TestCase


class Test(TestCase):
    def setUp(self) -> None:
        self.app = create_app('../secret.json').test_client()

    def test_get_book(self):
        result = self.app.get('/api/book')
        self.assertEqual(result.status_code, 200)
