from flask import Blueprint, request
from Backend.models import User
from Backend import psql

ussd = Blueprint("ussd",__name__)

@ussd.route("/launch", methods=['GET', 'POST'])
def ussd_launch():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    
    if text == '':
        #TODO: Check if user exists 
        user = User.check_user_exists(phone_number)
        if user:
            response = f"CON Welcome back {user.first_name} \n"
            response += "1. Send Money \n"
            response += "2. Withdraw Money \n"
            response += "3. Top up Account \n"
            text = '2'
        else:
            response = "CON Welcome to Badili. The future of mobile money\n"
            response += "1. Register Account"
        
    elif text == '1':
        response = "CON Enter your National ID number"
        # user = User("00000001", phone_number, "6341")
        # if user:
        #     print("User is correct")
        #     print(user)
        #     psql.session.add(user)
        #     psql.session.commit()
    
    
    return response