class Payment:
    def __new__(cls, config, payment):
        cls.config = config
        country = cls.config.get('COUNTRY')
        if country == "Kenya":
            return Mpesa(payment, cls.config.get('MPESA_SHORT_CODE'), cls.config.get('MPESA_CONFIRMATION_URL'), cls.config.get('MPESA_VALIDATION_URL'))

class Mpesa:
    def __init__(self, mpesa_api, short_code, confirmation_url, validation_url):
        self.mpesa_api = mpesa_api
        self.short_code = short_code
        self.confirmation_url = confirmation_url
        self.validation_url = validation_url  
        self.register_mpesa()

    def register_mpesa(self):
        reg_data={
            "shortcode": self.short_code,
            "response_type": "Completed",
            "confirmation_url": self.confirmation_url,
            "validation_url": self.validation_url
        }
        response = self.mpesa_api.C2B.register(**reg_data)  
        print(response)
    
    def make_mock_payment(self, amount, msisdn, bill_ref_number):
        test_data={
            "shortcode": self.short_code,
            "command_id": "CustomerPayBillOnline",
            "amount": amount,
            "msisdn": msisdn,
            "bill_ref_number": bill_ref_number
        }
        return self.mpesa_api.C2B.simulate(**test_data)