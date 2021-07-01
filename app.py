import json

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(test: bool = False):
    app = Flask(__name__)  # pylint: disable=redefined-outer-name

    secret_path = '../secret.json' if test == 1 else 'secret.json'
    with open(secret_path) as secret:
        secret = json.load(secret)
        app.config['MONGO_URI'] = secret['MONGO_URI']

    from api.routes.book import book  # pylint: disable=import-outside-toplevel,cyclic-import

    app.register_blueprint(book)
    mongo.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
