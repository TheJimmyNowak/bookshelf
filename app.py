from flask import Flask
from flask_pymongo import PyMongo
import logging

import config

import os

mongo = PyMongo()
logger = None #to logging.getLogger() logging should be configed (variable setup in create_app()


def create_app():
    app = Flask(__name__)  # pylint: disable=redefined-outer-name

    app.config.from_object(config)

    from api.routes.book import book  # pylint: disable=import-outside-toplevel,cyclic-import
    from api.routes.auth import auth  # pylint: disable=import-outside-toplevel

    app.register_blueprint(book)
    app.register_blueprint(auth)

    mongo.init_app(app)

    logging.basicConfig(level=logging.DEBUG)
    global logger
    logger = logging.getLogger()
    logger.info("App has been created")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()