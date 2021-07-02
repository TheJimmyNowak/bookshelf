import json
from unittest import TestCase
from unittest.mock import patch

from api.util.jwt_token import generate_jwt_token
from app import create_app


@patch('api.routes.book.mongo')
class Test(TestCase):
    def setUp(self) -> None:
        self.app = create_app().test_client()

    def test_get_book(self, mongo_mock):
        mongo_mock.db.books.find_one.return_value = dict()
        result = self.app.get('/api/book/60d96e139525b72cb24b71f7')

        self.assertEqual(result.json, dict())  # Check if result is emptydict
        self.assertEqual(result.status_code, 200)  # Check if status code is 200

        result = self.app.get('/api/book')
        self.assertEqual(result.status_code, 405)

    def test_get_book_by_localization(self, mongo_mock):
        test_entry = [{
            "_id": {
                "$oid": "60dc619397073050db7ad9c4"
            },
            "author": "Lenin",
            "conditon": "fadf",
            "location": {
                "coordinates": [
                    73.23,
                    21.2
                ],
                "type": "Point"
            },
            "name": "dłupa"
        }]

        mongo_mock.db.books.find.return_value = test_entry

        result = self.app.get('/api/book/73.23/21.2/1000000.0')

        self.assertEqual(result.json, test_entry)
        self.assertEqual(result.status_code, 200)

        result = self.app.get('/api/book/190.1/42.0/10.0')
        self.assertEqual(result.status_code, 400)

    def test_add_book(self, mongo_mock):
        public_id = '1ea4d7c6-ab97-41fe-bca4-f144002fbe6a'
        mongo_mock.db.books.find_one({'public_id': public_id})
        result = self.app.post('/api/book')

        self.assertEqual(result.status_code, 401)

        content = {
            "name": "TestName"
        }
        token = generate_jwt_token(public_id, 'SECRET')
        result = self.app.post('/api/book',
                               data=json.dumps(content),
                               content_type='application/json',
                               headers={
                                   'X-Access-Token': token}
                               )

        self.assertEqual(result.status_code, 400)

        content['author'] = "TestAuthor"
        content['condition'] = "Good"

        result = self.app.post('/api/book',
                               data=json.dumps(content),
                               content_type='application/json',
                               headers={'X-Access-Token': token})

        self.assertTrue(mongo_mock)
        self.assertEqual(result.status_code, 201)
