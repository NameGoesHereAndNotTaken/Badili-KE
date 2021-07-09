from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Backend.config import config
from middleware import Middleware

psql = SQLAlchemy()
migrate = Migrate()
middleware = Middleware()

def create_app(load_config):
    app = Flask(__name__)
    app.config.from_object(config[load_config])

    psql.init_app(app)
    migrate.init_app(app, psql)
    middleware.init_app(app)

    from Backend.USSD.v1.routes import ussd
    
    app.register_blueprint(ussd)

    return app