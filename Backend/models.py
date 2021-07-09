from Backend import psql, middleware
from flask import current_app

class User(psql.Model):
    id = psql.Column(psql.Integer, primary_key=True)
    first_name = psql.Column(psql.String(100), nullable=False)
    last_name = psql.Column(psql.String(100), nullable=False)
    id_number = psql.Column(psql.String(50), nullable=False)
    country_code = psql.Column(psql.String(10))
    phone_number = psql.Column(psql.String(15), nullable=False)
    pin = psql.Column(psql.String(100), nullable=False)
    public_key = psql.Column(psql.String(50), nullable=False)
    secret = psql.Column(psql.String(50), nullable=False)
    currencies = psql.Column(psql.String(500))
    
    def __init__(self, id_number, phone_number, pin):
        user, response = middleware.get_user_info(id_number)
        stellar_account, response = middleware.create_account_on_stellar(pin)

        if user and stellar_account:
            self.first_name = user['first_name']
            self.last_name = user['last_name']
            self.id_number = user['id_number']
            self.country_code = current_app.config.get("COUNTRY_CODE")
            self.phone_number = phone_number
            self.currencies = current_app.config.get("COUNTRY_CODE") + ","
            self.public_key = stellar_account['public_key']
            self.pin = stellar_account['secret']
