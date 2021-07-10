import os

class Config():
    SECRET_KEY = "OQ@FVuEtE2033>Kw73SA!dAy#6ey&fppojkK@<f52@mIdQOfIzKBTyQN!eWg6y2uxtM19lGN>5#mzsDEk2BvraxINa41Q+Fc0s!"
    DEBUG = True
    AFRICASTALKING_API = "38414b7e46837fb6adfd1051b39c5ad4100cf1e05a0bc80cceaec9409f008bf4"
    AFRICASTALKING_USERNAME = "grishon"

    APP_KEY = "v5GO3ZgnpRZcfnlnXGRLfTrPHggmqIfg"
    APP_SECRET = "Tz0wsgFDLvGVLBJh"
    API_ENVIRONMENT = "sandbox"
    HORIZON_NETWORK = "https://horizon-testnet.stellar.org"
    STELLAR_ADMIN_PUBLIC_KEY = os.environ.get("STELLAR_PUBLIC_KEY")
    STELLAR_ADMIN_SECRET_KEY = os.environ.get("STELLAR_SECRET_KEY")
    TIMEZONE = os.environ.get("LOCAL_TIMEZONE")

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DEV_SQLALCHEMY_DATABASE_URI') 
    SQLALCHEMY_ECHO = False
    DEBUG = True

    AFRICASTALKING_USERNAME = "sandbox"
    AFRICASTALKING_API = "59529cb095537a85924844301b1e5508b9dba6c03b9e7ca7092a88cf37a25474"
    COUNTRY_CODE = "KE"

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_SQLALCHEMY_DATABASE_URI')

    APP_KEY = "v5GO3ZgnpRZcfnlnXGRLfTrPHggmqIfg"
    APP_SECRET = "Tz0wsgFDLvGVLBJh"
    API_ENVIRONMENT = "sandbox"


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
}
