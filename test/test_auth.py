import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from bson import ObjectId

from app import create_app


class Test(TestCase):
    def setUp(self) -> None:
        self.app = create_app().test_client()

    @patch('api.routes.auth.generate_jwt_token', return_value="faddf")
    @patch('api.routes.auth.mongo')
    def test_login(self, mongo_mock: MagicMock, token_generator_mock: MagicMock):
        password_hash = \
            'pbkdf2:sha256:260000$0FAXi0i12F3fLkBY$b29f073f5' \
            '4f637cb55560d8f1729cba79c88ef5ed0fc214b802f1affb3b27db2'

        mongo_mock.db.users.find_one.return_value = {
            '_id': ObjectId('60ddb307ee58b79d669a7a34'),
            'email': 'aaa@aaaa.pl',
            'name': 'fdafda',
            'password': password_hash,
            'public_id': '1ea4d7c6-ab97-41fe-bca4-f144002fbe6a'
        }


        request_content = {
            "email": "aaa@aaaa.pl",
            "password": "toor"
        }

        result = self.app.post('/api/login',
                               data=request_content,
                               content_type='multipart/form-data')
        self.assertEqual(result.status_code, 201)

    def test_login_wrong_data(self):
        result = self.app.post('/api/login')
        self.assertEqual(result.status_code, 401)

        content = {
            'email': 'test@mail.com'
        }
        result = self.app.post('/api/login',
                               data=json.dumps(content),
                               content_type='application/json')
        self.assertEqual(result.status_code, 401)

        content = {
            'password': 'very_secret_password'
        }
        result = self.app.post('/api/login',
                               data=json.dumps(content),
                               content_type='application/json')
        self.assertEqual(result.status_code, 401)

    @patch('api.routes.auth.mongo')
    def test_register(self, mongo_mock):
        mongo_mock.db.users.find_one.return_value = None
        request_content = {
            "email": "aaa@aaaa.pl",
            "password": "toor"
        }

        result = self.app.post('/api/register',
                               data=request_content,
                               content_type='multipart/form-data')
        self.assertEqual(result.status_code, 201)
        mongo_mock.db.users.insert_one.assert_called()
