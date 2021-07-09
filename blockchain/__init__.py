
import warnings
from stellar_sdk import Keypair, Server, TransactionBuilder
from werkzeug.security import generate_password_hash
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Stellar:
    def __init__(self, config):
        self.config = config
        self.masterkey = Keypair.from_secret(self.config.get('STELLAR_ADMIN_SECRET_KEY'))

    def create_account_on_blockchain(self, pin):
        keypair = Keypair.random()
        server = Server(horizon_url=self.config.get('HORIZON_NETWORK'))
        transaction = (
                TransactionBuilder(
                    source_account=server.load_account(self.masterkey.public_key),
                    network_passphrase=self.config.get('HORIZON_NETWORK'),
                    base_fee=server.fetch_base_fee()
                ).append_create_account_op(
                    destination=keypair.public_key,
                    starting_balance="5"
                ).set_timeout(1000).build()
        )
        transaction.sign(self.masterkey.secret)
        
        try:
            response = server.submit_transaction(transaction)
        except Exception as e:
            print(e)
            print(keypair.public_key)
            print(keypair.secret)
            response = e

        if response["successful"] != None:
            secret = self.hash_secret(pin, keypair.secret)
            return {'public_key': keypair.public_key, 'secret': secret}, {'status':'success'}
        else:
            return None, response

    def hash_secret(self, pin, secret):
        salt = generate_password_hash(pin)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(pin))

        f = Fernet(key)

        return f.encrypt(str.encode(secret))
        