import json

from flask import Blueprint, jsonify, Response
from ..models import mongo
from ..util.JSONEncoder import JSONEncoder

book = Blueprint('book', __name__)


@book.route('/api/book', methods=['GET'])
def get_book() -> Response:
    res = mongo.db.books.find_one()
    res = json.loads(JSONEncoder().encode(res))
    return jsonify(res)
