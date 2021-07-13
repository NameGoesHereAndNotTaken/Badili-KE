import re
from Backend.models import User
class Register:
    def __init__(self, menu_items, user_data):
        self.user_data = user_data
        self.menu_items = menu_items
        self.user = self.is_user_registered(self.user_data['phone_number'])
        self.determine_level()
        self.response = None
    
    def determine_level(self):
        if len(self.menu_items) == 1:
            self.level_one()
        
        if len(self.menu_items) == 2:
            self.level_two()

        if len(self.menu_items) == 3:
            self.level_three()

        if len(self.menu_items) == 4:
            self.level_four()

    def level_one(self):
        if self.menu_items[0] == '':
            if self.user:
                response = f"CON Welcome back {self.user.first_name} \n"
                response += "1. Send Money \n"
                response += "2. Withdraw Money \n"
                response += "3. Top up Account \n"
                self.response = response
            else:
                response = "CON Welcome to Badili. The future of mobile money\n"
                response += "1. Register Account"
                self.response = response
        else:
            if not self.user:                
                response = "CON Enter your National ID number"
                self.response = response

    def level_two(self):
        response = "CON Enter pin to secure your account"
        self.response = response

    def level_three(self):
        response = "CON Confirm pin"
        self.response = response

    def level_four(self):
        print(self.menu_items)
        pass

    def get_response(self):
        return self.response

    def get_text(self):
        return self.text

    @classmethod
    def is_user_registered(cls, phone_number):
        return User.check_user_exists(phone_number)
    
class SendMoney:
    def __init__(self, menu_items):
        self.menu_items = menu_items
        self.determine_level()

    def determine_level(self):
        if len(self.menu_items) == 1:
            self.level_one()
        elif len(self.menu_items) == 2:
            self.level_two()
    
    def level_one(self):
        response = "CON 1. Badili Account\n"
        response += "2. Stellar Address"
        self.response = response

    def level_two(self):
        if self.menu_items[1] == "1":
            response = "CON Enter Account Number of receipient"
        else:
            response = "CON Enter Stellar Address of receipient"
            
        self.response = response

    def level_three(self):
        pass

    def get_response(self):
        return self.response
class FundAccount:
    pass

class Withdraw:
    pass

class Account:
    pass

class Settings:
    pass