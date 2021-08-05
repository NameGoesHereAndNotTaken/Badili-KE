from Backend import psql, middleware, mpesa_api
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pytz, jwt

from werkzeug.security import generate_password_hash
class User(psql.Model):
    id = psql.Column(psql.Integer, primary_key=True)
    first_name = psql.Column(psql.String(100), nullable=False)
    last_name = psql.Column(psql.String(100), nullable=False)
    email = psql.Column(psql.String(159), nullable=True)
    id_number = psql.Column(psql.String(50), nullable=False)
    country_code = psql.Column(psql.String(10))
    phone_number = psql.Column(psql.String(15), nullable=True)
    pin = psql.Column(psql.String(150), nullable=True)
    password = psql.Column(psql.String(500), nullable=True)
    public_key = psql.Column(psql.String(100), nullable=False)
    secret = psql.Column(psql.String(500), nullable=False)
    currencies = psql.Column(psql.String(500))
    timestamp = psql.Column(psql.DateTime)
    
    def __init__(self, id_number, phone_number=None, email=None, pin=None, password=None):
        user, response = middleware.get_user_info(id_number)
        if password is None and email is None:
            stellar_account, response = middleware.create_account_on_stellar(pin)
        else:
            stellar_account, response = middleware.create_account_on_stellar(password)
            
        if user and stellar_account:
            self.first_name = user['first_name']
            self.last_name = user['last_name']
            self.id_number = user['id_number']
            self.country_code = current_app.config.get("COUNTRY_CODE")
            self.phone_number = phone_number 
            self.email = email
            self.currencies = current_app.config.get("COUNTRY_CODE") + ","
            self.public_key = stellar_account['public_key']
            self.pin = generate_password_hash(pin) if pin is not None else None
            self.password = generate_password_hash(password) if password is not None else None
            self.secret = stellar_account['secret']
            self.timestamp = datetime.now(pytz.timezone(current_app.config.get('TIMEZONE')))

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def encode_auth_token(self, user_id):
        '''
        Generate auth token for a user aftere sign up.
        '''
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=0),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            
            return jwt.encode(
                payload, 
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256' 
            )
        except Exception as e:
            return e

    @classmethod
    def check_user_exists(cls, phone_number):
        return User.query.filter_by(phone_number = phone_number).first()

    @classmethod
    def check_user_exists_by_email(cls, email):
        return User.query.filter_by(email = email).first()

    @classmethod
    def send_message(cls, message, phone_number):
        return middleware.send_message(message, phone_number)

    @classmethod
    def mock_deposit(cls, phone_number, amount):
        return middleware.mpesa_top_up_account(phone_number[1:], amount)

    @staticmethod
    def decode_auth_token(auth_token):
        try :
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, sign in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again.'

class Transaction(psql.Model):
    id = psql.Column(psql.Integer, primary_key=True)
    transaction_id = psql.Column(psql.String(100), nullable=False)
    timestamp = psql.Column(psql.DateTime)
    user_id = psql.Column(psql.ForeignKey('user.id'), nullable=False)

    def __init__(self, transaction_id, user_id):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.timestamp = datetime.now(pytz.timezone(current_app.config.get('TIMEZONE')))