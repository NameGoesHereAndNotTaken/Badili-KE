import os

class Config():
    SECRET_KEY = "OQ@FVuEtE2033>Kw73SA!dAy#6ey&fppojkK@<f52@mIdQOfIzKBTyQN!eWg6y2uxtM19lGN>5#mzsDEk2BvraxINa41Q+Fc0s!"
    DEBUG = True
    
    #Africa's Talking API's
    AFRICASTALKING_API = "38414b7e46837fb6adfd1051b39c5ad4100cf1e05a0bc80cceaec9409f008bf4"
    AFRICASTALKING_USERNAME = "grishon"

    #MPESA API's
    APP_KEY = "chJsIrnNZck2NiFA9gZmeZov4l2YRR5W"
    APP_SECRET = "74uSsrE7qRWmbVYY"
    API_ENVIRONMENT = "sandbox"
    MPESA_SHORT_CODE = os.environ.get("MPESA_SHORT_CODE")
    MPESA_CONFIRMATION_URL = os.environ.get("MPESA_CONFIRMATION_URL")
    MPESA_VALIDATION_URL = os.environ.get("MPESA_VALIDATION_URL")

    #Stellar Settings
    HORIZON_NETWORK = "https://horizon-testnet.stellar.org"
    STELLAR_ADMIN_PUBLIC_KEY = os.environ.get("STELLAR_PUBLIC_KEY")
    STELLAR_ADMIN_SECRET_KEY = os.environ.get("STELLAR_SECRET_KEY")

    #Country & Timezone settings
    TIMEZONE = os.environ.get("LOCAL_TIMEZONE")
    COUNTRY = os.environ.get("COUNTRY")

    #Appruve KYC Settings
    APPRUVE_API_KEY = os.environ.get("APPRUVE_TOKEN")
    APPRUVE_BASE_URL = os.environ.get("APPRUVE_BASE_URL")

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DEV_SQLALCHEMY_DATABASE_URI') 
    SQLALCHEMY_ECHO = False

    AFRICASTALKING_USERNAME = "sandbox"
    AFRICASTALKING_API = "59529cb095537a85924844301b1e5508b9dba6c03b9e7ca7092a88cf37a25474"
    COUNTRY_CODE = os.environ.get("COUNTRY_CODE")

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_SQLALCHEMY_DATABASE_URI')

    #Mpesa Settings -> To be changed for prod
    APP_KEY = "v5GO3ZgnpRZcfnlnXGRLfTrPHggmqIfg"
    APP_SECRET = "Tz0wsgFDLvGVLBJh"
    API_ENVIRONMENT = "sandbox"


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
}
