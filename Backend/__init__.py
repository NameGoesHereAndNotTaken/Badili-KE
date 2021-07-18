from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Backend.config import config
from middleware import Middleware
from flask_mpesa import MpesaAPI

psql = SQLAlchemy()
migrate = Migrate()
middleware = Middleware()
mpesa_api = MpesaAPI()

def create_app(load_config):
    app = Flask(__name__)
    app.config.from_object(config[load_config])

    psql.init_app(app)
    migrate.init_app(app, psql)
    mpesa_api.init_app(app)
    middleware.init_app(app, mpesa_api)

    from Backend.USSD.v1.routes import ussd
    
    app.register_blueprint(ussd)

    return app