import uuid
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, request, make_response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app, mongo

auth = Blueprint('auth', __name__)
app = create_app(init_db=False)


@auth.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = mongo.db.users.find_one({'email': auth.get('email')})

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user['password'], auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user['public_id'],
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@auth.route('/register', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user = mongo.db.users.find_one({'email': data.get('email')})

    if not user:
        # database ORM object
        user = {
            'public_id': str(uuid.uuid4()),
            'name': name,
            'email': email,
            'password': generate_password_hash(password)
        }

        mongo.db.users.insert_one(user)
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
