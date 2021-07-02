from unittest import TestCase

from app import create_app


class Test(TestCase):
    def setUp(self) -> None:
        self.app = create_app().test_client()

    def test_token_required(self):
        # TODO

        pass
