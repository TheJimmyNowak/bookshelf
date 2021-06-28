import json
import logging

from bson import ObjectId
from flask import Blueprint, jsonify, Response, request
from api.models import mongo
from api.util.JSONEncoder import JSONEncoder

book = Blueprint('book', __name__)
logger = logging.getLogger("books")


@book.route('/api/book/<book_id>', methods=['GET'])
def get_book(book_id: str) -> Response:
    res = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    res = json.loads(JSONEncoder().encode(res))
    return jsonify(res)


@book.route('/api/book', methods=["POST"])
def add_book() -> Response:
    content = request.json

    if len(content['name']) < 0 or len(content['author']) < 0:
        logger.debug("Endpoint called without proper body")
        return Response(status=400)

    mongo.db.books.insert_one(content)

    return Response(status=500)
