import re
from Backend.models import User
from Backend import psql

class Register:
    def __init__(self, menu_items, user_data):
        self.user_data = user_data
        self.menu_items = menu_items
        self.user = self.is_user_registered(self.user_data['phone_number'])
        self.response = None
        self.determine_level()
        
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
        id_number = self.menu_items[1]
        pin = self.menu_items[2]
        confirm_pin = self.menu_items[3]
        phone_number = self.user_data['phone_number']
        if pin == confirm_pin:
            new_user = User(id_number, phone_number, pin)
            psql.session.add(new_user)
            psql.session.commit()
            response = "END Successfully created account"
            self.response = response
        else:
            response = "END Error. Pins don't match. Try again"
            self.response = response

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
        elif len(self.menu_items) == 3:
            self.level_three()
        elif len(self.menu_items) == 4:
            self.level_four()
    
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
        phone_number = self.menu_items[2]
        user = Register.is_user_registered(phone_number)
        if user:
            response = "CON Enter amount to send"
        else:
            response = "END User does not exist. Make sure you have the correct account number"

        self.response = response

    def level_four(self):
        amount = self.menu_items[3]
        if float(amount) > 0 and float(amount) < 10000:
            response = "CON Enter your pin"
        else:
            response = "END Amount is not valid"
        self.response = response    

    def get_response(self):
        return self.response

class FundAccount:
    def __init__(self, menu_items, user_data):
        self.menu_items = menu_items
        self.user_data = user_data
        self.response = None
        self.determine_level()

    def determine_level(self):
        if len(self.menu_items) == 1:
            self.level_one()
        
    def level_one(self):
        message_status = User.send_message(
            f"Go to MPESA, Send amount to PAYBILL 230054 with ACCOUNT NO as {self.user_data['phone_number']}. We will send you a confirmation.",
            [self.user_data['phone_number']]
        )
        print("Messssssssaaage is")
        print(message_status)
        if message_status['status'] == 'success':
            response = "END We have sent you the next process to follow on your mobile number"
        else:
            response = "END Sorry something wrong occurred. Please try again later"

        self.response = response

    def get_response(self):
        return self.response


class Withdraw:
    pass

class Account:
    pass

class Settings:
    pass