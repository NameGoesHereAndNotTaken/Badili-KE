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
        user = User("00000001", phone_number, "6341")
        if user:
            print("User is correct")
            print(user)
            psql.session.add(user)
            psql.session.commit()
        else:
            print("User not exists")
            print(user)

        # if not user:
        #     response = "CON Welcome to Badili.co Move money anywhere.\n"
        #     response += "1. Account Registration"
        # else:
        #     response = f"CON Welcome back {user.first_name} \n"
        #     response += "1. Send Money \n"
        #     response += "2. Withdraw Money \n"
        #     response += "3. Top up Account \n"
    
    return response