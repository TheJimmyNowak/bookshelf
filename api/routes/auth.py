import uuid

from flask import Blueprint, request, make_response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from api.util.jwt_token import generate_jwt_token
from app import create_app, mongo

auth = Blueprint('auth', __name__)
app = create_app()


@auth.route('/api/login', methods=['POST'])
def login():
    auth_data = request.form

    are_required_data_passed = \
        not (not auth_data or not auth_data.get('email') or not auth_data.get('password'))

    if not are_required_data_passed:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = mongo.db.users.find_one({'email': auth_data.get('email')})

    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if not check_password_hash(user['password'], auth_data.get('password')):
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
        )

    token = generate_jwt_token(user['public_id'], app.config['JWT_KEY'])
    return make_response(jsonify({'token': token}), 201)


@auth.route('/api/register', methods=['POST'])
def register():
    data = request.form

    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user_by_email = mongo.db.users.find_one({'email': data.get('email')})
    user_by_name = mongo.db.users.find_one({'name': data.get('name')})
    if user_by_email or user_by_name:
        return make_response('User already exists. Please Log in.', 202)

    user = {
        'public_id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'password': generate_password_hash(password)
    }

    mongo.db.users.insert_one(user)
    return make_response('Successfully registered.', 201)
