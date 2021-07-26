from unittest import TestCase
from unittest.mock import patch

from bson import ObjectId

from app import create_app


@patch('api.routes.user.mongo')
class Test(TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.test_app = self.app.test_client()

    def test_get_user_by_id(self, mongo_mock):
        mongo_mock.db.users.find_one.return_value = {
            "_id": ObjectId("60ddb307ee58b79d669a7a84"),
            "email": "sex@pl.pl",
            "name": "root",
            "public_id": "1ea4d7c6-ab97-41fe-bca4-f144002fbe6a"
        }

        result = self.test_app.get('/api/user/60ddb307ee58b79d669a7a84')
        self.assertEqual(result.status_code, 200)

    def test_get_user_by_id_bad_id(self, mongo_mock):
        result = self.test_app.get('/api/user/60ddb307ee58b79d669a7a8')
        self.assertEqual(result.status_code, 400)
