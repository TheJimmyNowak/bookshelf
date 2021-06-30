from flask import Flask
import json
import os


def create_app(secret_path='secret.json'):
    app = Flask(__name__)

    from api.routes.book import book
    app.register_blueprint(book)

    if not os.path.exists(secret_path):
        print("Secrets are not setted up")
        return app

    with open(secret_path) as secret:
        secret = json.load(secret)

        from api.models import mongo

        app.config["MONGO_URI"] = secret['connection-string']

    mongo.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
