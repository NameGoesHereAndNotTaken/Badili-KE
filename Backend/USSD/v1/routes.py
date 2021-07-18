from flask import Blueprint, request
from Backend.models import User
from Backend import psql
from .menu import Register, SendMoney, FundAccount

ussd = Blueprint("ussd",__name__)

@ussd.route("/launch", methods=['GET', 'POST'])
def ussd_launch():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")
    menu_items = get_menu_items(text)
    user_data = {
        'session_id':session_id,
        'service_code':service_code,
        'phone_number':phone_number,
    }

    if menu_items[0] == '':
        register  = Register(menu_items, user_data)
        response = register.get_response()
    elif menu_items[0] == "1":
        user = Register.is_user_registered(phone_number)
        if not user:
            register  = Register(menu_items, user_data)
            response = register.get_response()
        else:
            send_money = SendMoney(menu_items)
            response = send_money.get_response()
    elif menu_items[0] == '3':
        fund_account = FundAccount(menu_items, user_data)
        response = fund_account.get_response()
        
    return response

@ussd.route('/payments/ke/mobile-money/confirmation', methods=['POST'])
def mpesa_confirmation():
    data = request.data
    print("We are in this part we want!!!!!!!!")
    print(data)


def get_menu_items(text):
    return text.split('*')

def is_first_entry(menu_items):
    return True if len(menu_items) == 1 and menu_items[0] == '' else False

def is_second_entry(menu_items):
    return True if len(menu_items) == 2 else False

def register_account_part_one(menu_items):
    return True if menu_items[0] == "1" and menu_items[1] != '' else False

def register_account_part_two(menu_items):
    return True if menu_items[0] == "1" and menu_items[1] != '' and menu_items[2] != '' else False