from flask import Flask
import json


def create_app(secret_path='secret.json'):
    app = Flask(__name__)
    with open(secret_path) as secret:
        secret = json.load(secret)

        from api.routes.book import book
        from api.models import mongo

        app.register_blueprint(book)
        app.config["MONGO_URI"] = secret['connection-string']

    mongo.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
