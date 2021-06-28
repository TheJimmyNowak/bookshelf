from app import create_app
from unittest import TestCase
from unittest.mock import Mock, patch


class Test(TestCase):
    def setUp(self) -> None:
        self.app = create_app('../secret.json').test_client()

    @patch('api.routes.book.mongo')
    def test_get_book(self, mongo_mock):
        mongo_mock.db.books.find_one.return_value = {}
        result = self.app.get('/api/book/1')

        self.assertEqual(mongo_mock.called, True)
        self.assertEqual(result, {})