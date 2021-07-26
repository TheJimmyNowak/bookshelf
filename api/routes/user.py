import json
import logging
import traceback

import bson.errors
from bson import ObjectId
from flask import Blueprint, jsonify, Response

from api.util.json_encoder import JSONEncoder
from app import mongo

user = Blueprint('user', __name__)
LOGGER = logging.getLogger()


@user.route('/api/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id: str) -> Response:
    try:
        user_id = ObjectId(user_id)
    except bson.errors.InvalidId:
        LOGGER.exception(traceback.format_exc())
        return Response(status=400)

    result = mongo.db.users.find_one({'_id': user_id}, {'password': 0})
    result = json.loads(JSONEncoder().encode(result))
    return jsonify(result)
