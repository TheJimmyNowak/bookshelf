import pymongo
import json

secrets = open("secret.json")
secrets = json.load(secrets)

client = pymongo.MongoClient(secrets['connection-string'])
db = client.bookshelf

db.create_collection("books")
db.create_collection("users")
