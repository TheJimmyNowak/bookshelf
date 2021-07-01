import json

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()
db = mongo.db


def create_app(init_db: bool = True):
    app = Flask(__name__)  # pylint: disable=redefined-outer-name

    if init_db:
        secret_path = 'secret.json'
        with open(secret_path) as secret:
            secret = json.load(secret)
            app.config['MONGO_URI'] = secret['MONGO_URI']

        mongo.init_app(app)
    app.config['SECRET_KEY'] = 'SEX'

    from api.routes.book import book  # pylint: disable=import-outside-toplevel,cyclic-import
    from api.routes.auth import auth

    app.register_blueprint(book)
    app.register_blueprint(auth)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
