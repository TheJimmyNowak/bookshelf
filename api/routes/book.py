import json

from flask import Blueprint, jsonify, Response
from api.models import mongo
from api.util.JSONEncoder import JSONEncoder

book = Blueprint('book', __name__)


@book.route('/api/book', methods=['GET'])
def get_book() -> Response:
    """
    It's just example. To redesign in future
    :return:
    """
    res = mongo.db.books.find_one()
    res = json.loads(JSONEncoder().encode(res))
    return jsonify(res)
