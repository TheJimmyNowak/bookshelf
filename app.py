import logging
import sys

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

import config

mongo = PyMongo()


def create_app():
    app = Flask(__name__)  # pylint: disable=redefined-outer-name
    CORS(app)

    app.config.from_object(config)

    from api.routes.book import book  # pylint: disable=import-outside-toplevel,cyclic-import
    from api.routes.auth import auth  # pylint: disable=import-outside-toplevel

    app.register_blueprint(book)
    app.register_blueprint(auth)

    mongo.init_app(app)

    logging.basicConfig(level=logging.DEBUG, filename="app.log", format='%(asctime)s %(message)s')
    logger = logging.getLogger()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
