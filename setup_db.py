import json
import pymongo
import logging

logger = logging.getLogger()

logger.info("Reading secrets")
with open("secret.json") as secrets:
    secrets = json.load(secrets)

logger.info("Connecting with DB")
client = pymongo.MongoClient(secrets['connection-string'])
db = client.bookshelf

logger.info("Creating collections")
db.create_collection("books")
db.create_collection("users")

logger.info("Creating indexes")
db.books.create_index([("location", pymongo.GEOSPHERE)])

logger.info("DB setted up")
