import json
import pymongo
import logging

LOGGER = logging.getLogger()

LOGGER.info("Reading secrets")
with open("secret.json") as secrets:
    secrets = json.load(secrets)

LOGGER.info("Connecting with DB")
client = pymongo.MongoClient(secrets['connection-string'])
db = client.bookshelf

LOGGER.info("Creating collections")
db.create_collection("books")
db.create_collection("users")

LOGGER.info("Creating indexes")
db.books.create_index([("location", pymongo.GEOSPHERE)])

LOGGER.info("DB setted up")
