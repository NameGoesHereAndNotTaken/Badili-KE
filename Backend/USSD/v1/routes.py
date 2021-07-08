from flask import Blueprint, request
from flask.wrappers import Response

ussd = Blueprint("ussd",__name__)

@ussd.route("/launch", methods=['GET', 'POST'])
def ussd_launch():
    sessiond_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    if text == '':
        response = "CON Welcome to Badili.co Move money anywhere.\n"
        response += "1. Account Registration"
    
    return response