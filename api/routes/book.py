import json
import logging
from bson.json_util import dumps, ObjectId
from flask import Blueprint, jsonify, Response, request

from app import mongo
from api.util.jwt_token import token_required
from api.util.json_encoder import JSONEncoder

book = Blueprint('book', __name__)
logger = logging.getLogger()


@book.route('/api/book/<book_id>', methods=['GET'])
def get_book_id(book_id: str) -> Response:
    result = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    result = json.loads(JSONEncoder().encode(result))
    logger.info("get_book_id called, returning:\n {}".format(result))
    return jsonify(result)


@book.route('/api/book/<float:longitude>/<float:latitude>/<float:max_distance>')
def get_book_by_localization(longitude: float, latitude: float, max_distance: float) -> Response:
    is_longitude_correct = -180 < longitude < 180
    is_latitude_correct = -90 < latitude < 90

    if not is_longitude_correct or not is_latitude_correct:
        return Response(status=400)

    result = mongo.db.books.find({
        "location": {
            "$near":
                {
                    "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                    "$maxDistance": max_distance
                }
        }
    })

    result = dumps(result)
    result = json.loads(result)
    logger.info("get_book_by_localization called, returning:\n {}".format(result))
    return jsonify(result)


@book.route('/api/book', methods=["POST"])
@token_required
def add_book() -> Response:
    content = request.json

    is_required_data_passed: bool = \
        content is not None and "name" in content and "author" in content

    if is_required_data_passed:
        mongo.db.books.insert_one(content)
        logger.info("add_book called, {} was added".format(content))
        return Response(status=201)

    return Response(status=400)
