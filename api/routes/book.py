
from flask import Blueprint, jsonify
from ..models import mongo
from ..util.JSONEncoder import JSONEncoder

book = Blueprint('book', __name__)


@book.route('/api/book', methods=['GET'])
def get_book():
    res = mongo.db.books.find_one()
    res = JSONEncoder().encode(res)
    return jsonify(res)
