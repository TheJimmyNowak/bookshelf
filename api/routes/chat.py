import json
import logging
from bson.json_util import dumps, ObjectId
from flask import Blueprint, jsonify, Response, request
from flask_pymongo import PyMongo

from app import mongo
from api.util.jwt_token import token_required
from api.util.json_encoder import JSONEncoder

import datetime

chat = Blueprint('chat', __name__)
logger = logging.getLogger()


@chat.route('/api/chat/<user_id>', methods=['GET'])
@token_required
def get_chat_history(chat_id: str):
    result = mongo.db.chats.find_one({"_id": ObjectId(chat_id)})
    logger.info("get_chat_history called")
    return result


@chat.route('/api/chat/', methods=['POST'])
@token_required
def send_message() -> Response:
    content = request.json
    chat_id = content["chat_id"]
    user_id = content["user_id"]
    message = content["message"]
    if message is None:
        return Response(status=400)
    if mongo.db.chats.find_one({"_id": ObjectId(chat_id)}) is None:
        logger.info("Chat with specified chat_id doesn't exist")
        return Response(status=404)
    print(message)
    mongo.db.chats.update_one({"_id": ObjectId(chat_id)}, {"$push": {
        "messages":
            {
                "date": datetime.datetime.now(),
                "user": user_id,
                "content": message
            }
    }
    })
    return Response(status=201)


@chat.route('/api/chat/create/', methods=['POST'])
@token_required
def create_chat() -> Response:
    mongo.db.chats.insert_one({"users":
        {
            "user_1": request.json["user_1"],
            "user_2": request.json["user_2"]
        },
        "messages": []
    })
    return Response(status=201)
