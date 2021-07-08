from Backend import psql
from flask import current_app

class User(psql.Model):
    id = psql.Column(psql.Integer, primary_key=True)
    first_name = psql.Column(psql.String(100), nullable=False)
    last_name = psql.Column(psql.String(100), nullable=False)
    id_number = psql.Column(psql.String(50), nullable=False)
    country_code = psql.Column(psql.String(10), default=current_app.config.get("COUNTRY_CODE"), nullable=False)
    phone_number = psql.Column(psql.String(15), nullable=False)
    pin = psql.Column(psql.String(100), nullable=False)
    public_key = psql.Column(psql.String(50), nullable=False)
    secret = psql.Column(psql.String(50), nullable=False)
    currencies = psql.Column(psql.String(500), default="{'code':"+current_app.config.get("COUNTRY_CODE")+"}")
    