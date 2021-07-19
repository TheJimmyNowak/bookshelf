from datetime import datetime, timedelta
from functools import wraps
from typing import Callable
import traceback

import jwt
from flask import request, jsonify
from app import mongo


def generate_jwt_token(public_id: str, jwt_key: str, expiration_time=30):
    token = jwt.encode({
        'public_id': public_id,
        'exp': datetime.utcnow() + timedelta(minutes=expiration_time)
    }, jwt_key)
    return token


def token_required(func: Callable) -> Callable:
    from app import create_app  # pylint: disable=import-outside-toplevel

    app = create_app()

    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, app.config['JWT_KEY'], algorithms="HS256")
            mongo.db.users.find_one({'public_id': data['public_id']})
        except Exception as e:
            print(e)
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401

        return func(*args, **kwargs)

    return decorated
