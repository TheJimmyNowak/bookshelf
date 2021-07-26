import json
import logging
import re
import traceback

import bson.errors
from bson.json_util import dumps, ObjectId
from flask import Blueprint, jsonify, Response, request

from app import mongo
from api.util.jwt_token import token_required
from api.util.json_encoder import JSONEncoder

book = Blueprint('book', __name__)
LOGGER = logging.getLogger()


@book.route('/api/book/<book_id>', methods=['GET'])
def get_book_id(book_id: str) -> Response:
    result = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    result = json.loads(JSONEncoder().encode(result))
    LOGGER.info("get_book_id called, returning: {}".format(result))
    return jsonify(result)


@book.route('/api/book/filter', methods=['GET'])
def get_book_by_filter() -> Response:
    name = request.args.get('name') if request.args.get('name') else ""
    author = request.args.get('author') if request.args.get('author') else ""

    name_regex = re.compile(".*" + name + ".*", re.IGNORECASE)
    author_regex = re.compile(".*" + author + ".*", re.IGNORECASE)
    result = list(mongo.db.books.find({
        'title': name_regex,
        'author': author_regex
    }))
    result = json.loads(JSONEncoder().encode(result))
    return jsonify(result)


@book.route('/api/book/<float:longitude>/<float:latitude>/<float:max_distance>', methods=['GET'])
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
    return jsonify(result)


@book.route('/api/book', methods=["POST"])
@token_required
def add_book(user) -> Response:
    content = request.json

    is_required_data_passed: bool = \
        content is not None and "title" in content and "author" in content

    if is_required_data_passed:
        content['owner'] = ObjectId(user['_id'])
        mongo.db.books.insert_one(content)
        LOGGER.info("add_book called, {} was added".format(content['title']))
        return Response(status=201)

    return Response(status=400)


@book.route('/api/book/<book_id>', methods=['DELETE'])
@token_required
def remove_book_by_id(book_id: str, user) -> Response:
    try:
        owner_id = mongo.db.books.find_one({"_id": ObjectId(book_id)},
                                           {"owner": 1, "_id": 0})['owner']
        if ObjectId(owner_id) == user['_id']:
            mongo.db.books.delete_one({"_id": ObjectId(book_id)})
            LOGGER.info("Book {} has been deleted".format(book_id))
            return Response(status=200)

    except bson.errors.InvalidId:
        LOGGER.exception(traceback.format_exc())

    return Response(status=400)
