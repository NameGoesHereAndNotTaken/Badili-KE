import os

from blockchain import Stellar

class Middleware:
    def __init__(self):
        self.app = None
        self.config = None
        self.stellar = None

    def init_app(self, app):
        with app.app_context():
            self.config = app.config
        self.stellar = Stellar(self.config)

    def get_user_info(self, id_number):
        if not id_number:
            return None, {'status':"Provide all required info."}
       
        user = {
            "first_name": "GRishon",
            "last_name":"Gikima",
            "id_number": id_number,
            "dob": "dob",
            "gender": "M"
        }
        return user, {'status': 'success'}

    def create_account_on_stellar(self, pin):
        return self.stellar.create_account_on_blockchain(pin)