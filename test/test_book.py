import json

from app import create_app
from unittest import TestCase
from unittest.mock import Mock, patch


@patch('api.routes.book.mongo')
class Test(TestCase):
    def setUp(self) -> None:
        self.app = create_app('../secret.json').test_client()

    def test_get_book(self, mongo_mock):
        mongo_mock.db.books.find_one.return_value = dict()
        result = self.app.get('/api/book/60d96e139525b72cb24b71f7')

        self.assertEqual(result.json, dict())  # Check if result is emptydict
        self.assertEqual(result.status_code, 200)  # Check if status code is 200

        result = self.app.get('/api/book')
        self.assertEqual(result.status_code, 405)

    def test_add_book(self, mongo_mock):
        result = self.app.post('/api/book')
        self.assertEqual(result.status_code, 400)

        content = {
            "name": "TestName"
        }
        result = self.app.post('/api/book', data=json.dumps(content), content_type='application/json')
        self.assertEqual(result.status_code, 400)

        content['author'] = "TestAuthor"
        content['condition'] = "Good"

        result = self.app.post('/api/book', data=json.dumps(content), content_type='application/json')
        self.assertTrue(mongo_mock)
        self.assertEqual(result.status_code, 201)
