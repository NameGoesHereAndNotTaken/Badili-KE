from flask import Blueprint, request, make_response, jsonify

from Backend.models import User, Transaction
from functools import wraps

from datetime import datetime, timedelta
import pytz, calendar

from Backend import psql 

api = Blueprint('api', __name__)


def login_required(function):
    @wraps(function)
    def wrapper(*f_args, **f_kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(' ')[1]  
            decoded_token = User.decode_auth_token(token)
            if decoded_token == 0:
                return make_response(jsonify({'status': 'fail', 'code':0, 'message':'Token expired. Please sign in again.'}))
            elif decoded_token == 1:
                return make_response(jsonify({'status': 'fail', 'code':1, 'message':'Authentication failed. Sign in with different credentials.'}))
            else:
                return function(*f_args, **f_kwargs)
        else:
            return make_response(jsonify({'status': 'fail', 'message': "Not authorized"})), 403
    return wrapper


@api.route('/api/v1/signin', methods=['POST'])
def api_signin():
    post_data = request.get_json(force=True)
    if not post_data or "email" not in post_data or "password" not in post_data or post_data["email"] == "" or post_data["password"] == "": 
        response = {'status': 'fail', 'message':'Please provide all required fields.'} 
        return make_response(jsonify(response)), 403
    email = post_data['email']
    password = post_data['password']
    user = User.check_user_exists_by_email(email)
    if user:
        if user.verify_password(password):
            token = user.encode_auth_token(user.id)
            response = {'status': 'success', 'message':'User signin successful', 'user': {"email": email, "names": user.first_name +" "+ user.last_name, 'stellar_address':user.public_key, 'auth_token': token} }
            return make_response(jsonify(response)), 200
        else:
            response = {'status': 'fail', 'message':'Email or password mismatch'}
            return make_response(jsonify(response)), 401
    else:
        response = {'status': 'fail', "message": "Account does not seem to exist"}
        return make_response(jsonify(response)), 403

@api.route('/api/v1/signup', methods=['POST'])
def api_signup():
    post_data = request.get_json(force=True)
    if not post_data or\
        "email" not in post_data or\
        "password" not in post_data or\
        "id_number" not in post_data or\
        "phone_number" not in post_data or\
        post_data["email"] == "" or\
        post_data["password"] == "" or\
        post_data["id_number"] == "" or\
        post_data["phone_number"] == "":

        response = {'status': 'fail', 'message':'Please provide all required fields.'} 
        return make_response(jsonify(response)), 403

    email = post_data['email']
    password = post_data['password']
    id_number = post_data['id_number']
    phone_number = post_data['phone_number']
    user = User.check_user_exists_by_email(email)
    if user:
        response = {'status': 'fail', 'message':'User with that email already exists.'} 
        return make_response(jsonify(response)), 409

    new_user = User(id_number, phone_number = phone_number, email = email, password=password)
    psql.session.add(new_user)
    psql.session.commit()
    print("This is the new user")
    print(new_user)
    if new_user:
        if new_user.verify_password(password):
            token = new_user.encode_auth_token(new_user.id)
            response = {'status': 'success', 'message':'User signin successful', 'user': {"email": email, "names": new_user.first_name +" "+ new_user.last_name, 'stellar_address':new_user.public_key, 'auth_token': token} }
            return make_response(jsonify(response)), 200
        else:
            response = {'status': 'fail', 'message':'Email or password mismatch'}
            return make_response(jsonify(response)), 401
    else:
        response = {'status': 'fail', "message": "Account does not seem to exist"}
        return make_response(jsonify(response)), 403
