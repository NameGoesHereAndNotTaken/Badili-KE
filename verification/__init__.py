import requests, warnings

class Appruve:
    def __init__(self, config):
        self.verification_type = ["national_id"]
        self.config = config
        self.url= self.config.get('APPRUVE_BASE_URL')

    def verify_national_id(self, id_number, type):
        if not self.valid_verification_type(type):
            warnings.warn("Not verification type we offer yet")
        
        if type == "national_id":
            return self._verify_id_number(id_number)
        else:
            #NOTE:Add more verification types
            return None

    def valid_verification_type(self, type):

        return None if type not in self.verification_type else True

    def _verify_id_number(self, id_number):
        data = {'id': id_number}
        headers = {'Content-Type': 'application/json', 'Authorization':'Bearer ' +self.config.get('APPRUVE_API_KEY')}
        response = requests.post(self.url+ "national_id",params=data,headers=headers)
        print("Response is")
        print(response.json())

        return response.json()

    @classmethod
    def get_valid_verification_types(cls):
        return cls.valid_verification_type

