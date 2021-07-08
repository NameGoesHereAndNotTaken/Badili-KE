from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from Backend.config import config

psql = SQLAlchemy()
migrate = Migrate()

def create_app(load_config):
    app = Flask(__name__)
    app.config.from_object(config[load_config])

    psql.init_app(app)
    migrate.init_app(app, psql)

    from Backend.USSD.v1.routes import ussd
    
    app.register_blueprint(ussd)

    return app