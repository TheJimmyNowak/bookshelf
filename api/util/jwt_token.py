from datetime import datetime, timedelta
from functools import wraps
from typing import Callable

import jwt
from flask import request, jsonify


def generate_jwt_token(public_id: str, jwt_key: str, expiration_time=30):
    token = jwt.encode({
        'public_id': public_id,
        'exp': datetime.utcnow() + timedelta(minutes=expiration_time)
    }, jwt_key)
    return token


def token_required(func: Callable) -> Callable:
    from app import mongo, create_app  # pylint: disable=import-outside-toplevel

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
            current_user = mongo.db.books.find_one({'public_id': data['public_id']})
        except Exception:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401

        return func(current_user, *args, **kwargs)

    return decorated
