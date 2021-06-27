from flask import Flask
from flask_pymongo import PyMongo
import json

secret = open('secret.json')
secret = json.load(secret)

app = Flask(__name__)

app.config["MONGO_URI"] = secret['connection-string']
mongo = PyMongo(app)

if __name__ == '__main__':
    app.run()
