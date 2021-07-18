import os
import uuid
from blockchain import Stellar
from verification import Appruve
from messaging import AT
from payments import Payment

class Middleware:
    def __init__(self):
        self.app = None
        self.config = None
        self.stellar = None
        self.payment_method = None

    def init_app(self, app, payment_method):
        with app.app_context():
            self.config = app.config
        self.stellar = Stellar(self.config)
        self.appruve = Appruve(self.config)
        self.africastalking = AT(self.config)
        self.payment_method = payment_method 
        self.payment = Payment(self.config, self.payment_method)

    def get_user_info(self, id_number):
        if not id_number:
            return None, {'status':"Provide all required info."}
        
        valid_verification_types = self.appruve.get_valid_verification_types()
        user = self.appruve.verify_national_id(id_number, "national_id")
        if user:
            user = {
                "first_name": user['first_name'],
                "last_name":user['last_name'],
                "id_number": user['id'],
                "dob": user['date_of_birth'],
                "gender": "gender"
            }
            return user, {'status': 'success'}
        else:
            return None, {'status': 'fail', 'message':'Womething wrong happened'}

    def create_account_on_stellar(self, pin):
        return self.stellar.create_account_on_blockchain(pin)

    def send_message(self,message, recipients):
        return self.africastalking.send_message(message, recipients)

    def mpesa_top_up_account(self, phone_account, amount):
        bill_ref = self._generate_bill_ref_number(phone_account)
        response = self.payment.make_mock_payment(amount, phone_account, bill_ref)
        if response["ResponseCode"] == "0":
            return bill_ref
        else:
            return None

    def _generate_bill_ref_number(self, phone_account):
        unique = uuid.uuid4().hex
        return str(phone_account) + str(unique)
        