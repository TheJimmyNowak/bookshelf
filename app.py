import json

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(test: bool = False):
    app = Flask(__name__)  # pylint: disable=redefined-outer-name

    if test == 0:
        secret_path = 'secret.json'
        with open(secret_path) as secret:
            secret = json.load(secret)
            app.config['MONGO_URI'] = secret['MONGO_URI']

        mongo.init_app(app)

    from api.routes.book import book  # pylint: disable=import-outside-toplevel,cyclic-import
    app.register_blueprint(book)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
