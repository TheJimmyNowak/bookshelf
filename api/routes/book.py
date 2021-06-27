from flask import Blueprint, jsonify
from ..models import mongo

book = Blueprint('book', __name__)


@book.route('/api/book', methods=['GET'])
def get_book():
    res = mongo.db.books.find_one()
    res.pop('_id')
    return jsonify(res)
