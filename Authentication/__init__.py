import warnings
from flask import current_app
from stellar_sdk import Keypair, Server, TransactionBuilder
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Authentication:
    def __init__(self, auth_model):
        self.user_model = auth_model


    def create_user(
        self,
        id_number=None,
        phone_number=None,
        pin=None,
    ):
        if not id_number:
            warnings.warn("Id number not provided")
        
        if not pin:
            warnings.warn("Pin not provided")

        # user_info = self.get_user_info(id_number)
        
        stellar_account = Stellar(pin)
        
        # first_name = user_info.first_name,
        #     last_name = user_info.last_name,
        #     id_number = user_info.id_number,

        user = self.user_model(
            first_name = "GRishon",
            last_name = "Gikima",
            id_number = id_number,
            country_code = current_app.config.get('COUNTRY_CODE'),
            phone_number = phone_number,
            pin = self._generate_user_pin_hash(pin),
            public_key = stellar_account.public_key,
            secret = stellar_account.secret,
            currencies = current_app.config.get('COUNTRY_CODE') + ","

            )
    
    def _generate_user_pin_hash(self, pin):
        return generate_password_hash(pin)

    @classmethod
    def generate_user_pin_hash(cls, pin):
        return generate_password_hash(pin)

class Stellar:
    def __init__(self, pin):
        self.pin = pin
        self.secret = None
        self.public_key = self.create_keypair()
        

    def get_hashed_secret(self):
        return self.secret

    def create_keypair(self):
        account = self._create_account_on_blockchain()
        if not account[0]:
            warnings.warn(account[1])
        else:
            return account[1]

    def _create_account_on_blockchain(self):
        keypair = Keypair.random()
        server = Server(horizon_url=current_app.config.get('HORIZON_NETWORK'))
        transaction = (
                TransactionBuilder(
                    source_account=server.load_account(current_app.config.get('STELLAR_ADMIN_PUBLIC_KEY')),
                    network_passphrase=current_app.config.get('HORIZON_NETWORK'),
                    base_fee=server.fetch_base_fee()
                ).append_create_account_op(
                    destination=keypair.public_key,
                    starting_balance="5"
                ).set_timeout(1000).build()
        )
        transaction.sign(current_app.config.get('STELLAR_ADMIN_SECRET_KEY'))
        try:
            response = server.submit_transaction(transaction)
        except Exception as e:
            response = e

        if response["successful"] != None:
            self.secret = self.hash_secret(self.pin, keypair.secret)
            return "Success", keypair
        else:
            return None, response



    def hash_secret(self, pin, secret):
        salt = Authentication.generate_user_pin_hash(pin)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(pin))

        f = Fernet(key)

        return f.encrypt(str.encode(secret))
        