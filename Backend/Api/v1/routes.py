from flask import Blueprint, request, make_response, jsonify

from Backend.models import User, Transaction
from functools import wraps

from datetime import datetime, timedelta
import pytz, calendar

from Backend import psql 

api = Blueprint('api', __name__)


def login_required(function):
    @wraps(function)
    def wrapper(*f_args, **f_kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(' ')[1]  
            decoded_token = User.decode_auth_token(token)
            if decoded_token == 0:
                return make_response(jsonify({'status': 'fail', 'code':0, 'message':'Token expired. Please sign in again.'}))
            elif decoded_token == 1:
                return make_response(jsonify({'status': 'fail', 'code':1, 'message':'Authentication failed. Sign in with different credentials.'}))
            else:
                return function(*f_args, **f_kwargs)
        else:
            return make_response(jsonify({'status': 'fail', 'message': "Not authorized"})), 403
    return wrapper


@api.route('/api/v1/signin', methods=['POST'])
def api_signin():
    post_data = request.get_json(force=True)
    if not post_data or "email" not in post_data or "password" not in post_data or post_data["email"] == "" or post_data["password"] == "": 
        response = {'status': 'fail', 'message':'Please provide all required fields.'} 
        return make_response(jsonify(response)), 403
    email = post_data['email']
    password = post_data['password']
    user = User.check_user_exists_by_email(email)
    if user:
        if user.verify_password(password):
            token = user.encode_auth_token(user.id)
            response = {'status': 'success', 'message':'User signin successful', 'auth_token': token, 'user': {"email": email, "names": user.first_name +" "+ user.last_name} }
            return make_response(jsonify(response)), 200
        else:
            response = {'status': 'fail', 'message':'Email or password mismatch'}
            return make_response(jsonify(response)), 401
    else:
        response = {'status': 'fail', "message": "Account does not seem to exist"}
        return make_response(jsonify(response)), 403

@api.route('/api/v1/signup', methods=['POST'])
def api_signup():
    post_data = request.get_json(force=True)
    if not post_data or\
        "email" not in post_data or\
        "password" not in post_data or\
        "id_number" not in post_data or\
        "phone_number" not in post_data or\
        post_data["email"] == "" or\
        post_data["password"] == "" or\
        post_data["id_number"] == "" or\
        post_data["phone_number"] == "":

        response = {'status': 'fail', 'message':'Please provide all required fields.'} 
        return make_response(jsonify(response)), 403

    email = post_data['email']
    password = post_data['password']
    id_number = post_data['id_number']
    phone_number = post_data['phone_number']
    user = User.check_user_exists_by_email(email)
    if user:
        response = {'status': 'fail', 'message':'User with that email already exists.'} 
        return make_response(jsonify(response)), 409

    new_user = User(id_number, phone_number = phone_number, email = email, password=password)
    psql.session.add(new_user)
    psql.session.commit()
    print("This is the new user")
    print(new_user)
    if new_user:
        if new_user.verify_password(password):
            token = new_user.encode_auth_token(new_user.id)
            response = {'status': 'success', 'message':'User signin successful', 'auth_token': token, 'user': {"email": email, "names": new_user.first_name +" "+ new_user.last_name} }
            return make_response(jsonify(response)), 200
        else:
            response = {'status': 'fail', 'message':'Email or password mismatch'}
            return make_response(jsonify(response)), 401
    else:
        response = {'status': 'fail', "message": "Account does not seem to exist"}
        return make_response(jsonify(response)), 403

# @api.route('/api/v1/apartment')
# @login_required
# def get_apartment():
#     data = get_user_details_from_header()
#     if data["user"] == "supervisor":
#         supervisor = Supervisor.query.get(data["id"])
#         apartment = Apartment.query.get(supervisor.apartment_id)
#         houses_occupied = House.query.filter_by(apartment_id = apartment.id).filter_by(status = True).count()
#         houses_empty = House.query.filter_by(apartment_id =apartment.id).filter_by(status = False).count()
#         response = {
#             "status": "success",
#             "apartment": {
#                 "id": apartment.id,
#                 "name": apartment.name,
#                 "location": apartment.location,
#                 "houses": apartment.houses,
#                 "image": apartment.image,
#                 "payment_methods": apartment.payment_methods,
#                 "occupied_houses": houses_occupied,
#                 "empty_houses": houses_empty
#             }
#         }
#         return make_response(jsonify(response)), 200

#     elif data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"]) 
#         apartment = Apartment.query.get(caretaker.apartment_id)
#         houses_occupied = House.query.filter_by(apartment_id = apartment.id).filter_by(status = True).count()
#         houses_empty = House.query.filter_by(apartment_id = apartment.id).filter_by(status = False).count()
#         response = {
#             "status": "success",
#             "apartment": {
#                 "id": apartment.id,
#                 "name": apartment.name,
#                 "location": apartment.location,
#                 "houses": apartment.houses,
#                 "image": apartment.image,
#                 "payment_methods": apartment.payment_methods,
#                 "occupied_houses": houses_occupied,
#                 "empty_houses": houses_empty
#             }
#         }
#         return make_response(jsonify(response)), 200
#     else:
#         response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#         return make_response(jsonify(response)), 401

# @api.route('/api/v1/tenants')
# @login_required
# def get_tenants():
#     data = get_user_details_from_header()
#     if data["user"] == "supervisor":
#         supervisor = Supervisor.query.get(data["id"])
#         apartment = Apartment.query.get(supervisor.apartment_id)
#         tenants = Tenant.query.filter_by(apartment_id = supervisor.apartment_id).with_entities(Tenant.id, Tenant.names, Tenant.occupation, Tenant.phone, Tenant.id_number, Tenant.moved_in, Tenant.debt, Tenant.amount, Tenant.house_id, Tenant.apartment_id).all()
#         tenants = [dict(zip(row.keys(), row)) for row in tenants]
#         response = {"status":"success", "tenants": tenants}
#         return make_response(jsonify(response)), 200


#     elif data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         tenants = Tenant.query.filter_by(apartment_id = caretaker.apartment_id).with_entities(Tenant.id, Tenant.names, Tenant.occupation, Tenant.phone, Tenant.id_number, Tenant.moved_in, Tenant.debt, Tenant.amount, Tenant.house_id, Tenant.apartment_id).all()
#         tenants = [dict(zip(row.keys(), row)) for row in tenants]
#         response = {"status":"success", "tenants": tenants}
#         return make_response(jsonify(response)), 200

#     else:
#         response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#         return make_response(jsonify(response)), 401

# @api.route('/api/v1/tenants/<int:id>')
# @login_required
# def get_tenant(id):
#     data = get_user_details_from_header()
#     tenant = Tenant.query.get(id)
#     if not tenant:
#         return make_response(jsonify({'status': 'fail', 'message': "Not found"})), 404
#     if data["user"] == "supervisor":
#         supervisor = Supervisor.query.get(data["id"])
#         if supervisor.apartment_id == tenant.apartment_id:
#             response = {
#                 "status": "success",
#                  "user": {
#                      "id": tenant.id,
#                      "names": tenant.names,
#                      "occupation": tenant.occupation,
#                      "phone": tenant.phone,
#                      "id_number": tenant.id_number,
#                      "moved_in": tenant.moved_in,
#                      "debt": tenant.debt,
#                      "amount": tenant.amount,
#                      "house_name": House.query.get(tenant.house_id).name,
#                      "house_id": tenant.house_id,
#                      "apartment_id": tenant.apartment_id
                    
#                 }
#             }
#             return make_response(jsonify(response)), 200
#         else:
#             response = {"status": "fail", "message": "Unauthorized Request"}
#             return make_response(jsonify(response)), 401
#     elif data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         if caretaker.apartment_id == tenant.apartment_id:
#             response = {
#                 "status": "success",
#                  "user": {
#                      "id": tenant.id,
#                      "names": tenant.names,
#                      "occupation": tenant.occupation,
#                      "phone": tenant.phone,
#                      "id_number": tenant.id_number,
#                      "moved_in": tenant.moved_in,
#                      "debt": tenant.debt,
#                      "amount": tenant.amount,
#                      "house_name": House.query.get(tenant.house_id).name,
#                      "house_id": tenant.house_id,
#                      "apartment_id": tenant.apartment_id
                    
#                 }
#             }
#             return make_response(jsonify(response)), 200
#         else:
#             response = {"status": "fail", "message": "Unauthorized Request"}
#             return make_response(jsonify(response)), 401

# @api.route('/api/v1/houses')
# @login_required
# def get_houses():
#     data = get_user_details_from_header()
#     if data["user"] == "supervisor":
#         supervisor = Supervisor.query.get(data["id"])
#         houses = House.query.filter_by(apartment_id = supervisor.apartment_id).with_entities(House.id, House.name, House.rent, House.deposit, House.floor, House.status, House.apartment_id).all()
#         houses = [dict(zip(row.keys(), row)) for row in houses]
#         response = {"status":"success", "houses": houses}
#         return make_response(jsonify(response)), 200
#     elif data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         houses = House.query.filter_by(apartment_id = caretaker.apartment_id).with_entities(House.id, House.name, House.rent, House.deposit, House.floor, House.status, House.apartment_id).all()
#         houses = [dict(zip(row.keys(), row)) for row in houses]
#         response = {"status":"success", "houses": houses}
#         return make_response(jsonify(response)), 200

#     else:
#         response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#         return make_response(jsonify(response)), 401

# @api.route('/api/v1/houses/<int:id>')
# @login_required
# def get_house(id):
#     data = get_user_details_from_header()
#     house = House.query.get(id)
#     if not house:
#         return make_response(jsonify({'status': 'fail', 'message': "Not found"})), 404
#     if data["user"] == "supervisor":
#         supervisor = Supervisor.query.get(data["id"])
#         if supervisor.apartment_id == house.apartment_id:
#             response = {
#                 "status": "success",
#                  "house": {
#                      "id": house.id,
#                      "name": house.name,
#                      "rent": house.rent,
#                      "deposit": house.deposit,
#                      "floor": house.floor,
#                      "status": house.status,
#                      "apartment_id": house.apartment_id
                    
#                 }
#             }
#             return make_response(jsonify(response)), 200
#         else:
#             response = {"status": "fail", "message": "Unauthorized Request"}
#             return make_response(jsonify(response)), 401
#     elif data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         if caretaker.apartment_id == house.apartment_id:
#             response = {
#                 "status": "success",
#                  "house": {
#                      "id": house.id,
#                      "name": house.name,
#                      "rent": house.rent,
#                      "deposit": house.deposit,
#                      "floor": house.floor,
#                      "status": house.status,
#                      "apartment_id": house.apartment_id
                    
#                 }
#             }
#             return make_response(jsonify(response)), 200
#         else:
#             response = {"status": "fail", "message": "Unauthorized Request"}
#             return make_response(jsonify(response)), 401

#     else:
#         response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#         return make_response(jsonify(response)), 401

# @api.route('/api/v1/tenant/<int:id>', methods=['PATCH'])
# @login_required
# def update_tenant(id):
#     data = get_user_details_from_header()
#     tenant = Tenant.query.get(id)
#     if not tenant:
#         return make_response(jsonify({'status': 'fail', 'message': "Not found"})), 404
#     if data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         if caretaker.apartment_id == tenant.apartment_id:
            
#             post_data = request.get_json(force=True)
#             if not post_data:
#                 return make_response(jsonify({'status': 'fail', 'message': "Please provide all required fields"})), 409
#             else:
#                 if "names" not in post_data and "occupation" not in post_data and "phone" not in post_data and "id_number" not in post_data:
#                     return make_response(jsonify({'status': 'fail', 'message': "Please provide all required fields"})), 422

#                 if "names" in post_data:
#                     tenant.names = post_data["names"]
                
#                 if "occupation" in post_data:
#                     tenant.occupation = post_data["occupation"]
                
#                 if "phone" in post_data:
#                     tenant.phone = post_data["phone"]

#                 if "id_number" in post_data:
#                     tenant.id_number = post_data["id_number"]

#                 mysql.session.add(tenant)
#                 mysql.session.commit()

#                 response = {
#                     "status": "success",
#                     "tenant": {
#                         "id": tenant.id,
#                         "names": tenant.names,
#                         "occupation": tenant.occupation,
#                         "phone": tenant.phone,
#                         "id_number": tenant.id_number,
#                         "moved_in": tenant.moved_in,
#                         "debt": tenant.debt,
#                         "amount": tenant.amount,
#                         "house_name": House.query.get(tenant.house_id).name,
#                         "house_id": tenant.house_id,
#                         "apartment_id": tenant.apartment_id
                        
#                     }
#                 }
#                 return make_response(jsonify(response)), 200
    
#         response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#         return make_response(jsonify(response)), 401

# @api.route('/api/v1/tenant/<int:id>', methods=['DELETE'])
# @login_required
# def delete_tenant(id):
#     data = get_user_details_from_header()
#     tenant = Tenant.query.get(id)
#     if not tenant:
#         return make_response(jsonify({'status': 'fail', 'message': "Not found"})), 404
#     if data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         if caretaker.apartment_id == tenant.apartment_id:
#             house = House.query.get(tenant.house_id)
#             house.status = False
#             deleted_tenant = DeletedTenant(names = tenant.names, occupation = tenant.occupation, phone = tenant.phone, id_number = tenant.id_number, moved_in = tenant.moved_in, moved_out = datetime.now(pytz.timezone('Africa/Nairobi')), debt_left_with = tenant.debt, apartment_id = tenant.apartment_id, house_id = tenant.house_id)
#             mysql.session.add(deleted_tenant)
#             mysql.session.add(house)
#             mysql.session.delete(tenant)
#             mysql.session.commit()
            
#             return make_response(jsonify({'status': 'success'})), 204
            
    
#     response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#     return make_response(jsonify(response)), 401

# @api.route('/api/v1/house/<int:id>', methods=['PATCH'])
# @login_required
# def update_house(id):
#     data = get_user_details_from_header()
#     house = House.query.get(id)
#     if not house:
#         return make_response(jsonify({'status': 'fail', 'message': "Not found"})), 404
#     if data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         if caretaker.apartment_id == house.apartment_id:
            
#             post_data = request.get_json(force=True)
#             if not post_data:
#                 return make_response(jsonify({'status': 'fail', 'message': "Please provide all required fields"})), 409
#             else:
#                 if "name" not in post_data and "rent" not in post_data and "floor" not in post_data:
#                     return make_response(jsonify({'status': 'fail', 'message': "Please provide all required fields"})), 422

#                 if "name" in post_data:
#                     if post_data['name'] == house.name or House.query.filter_by(apartment_id = house.apartment_id).filter_by(name = post_data["name"]).first():
#                         return make_response(jsonify({'status': 'fail', 'message': "Another house with that name exists."})), 304
#                     house.name = post_data["name"]
                
#                 if "rent" in post_data:
#                     house.occupation = post_data["rent"]
                
#                 if "floor" in post_data:
#                     house.phone = post_data["floor"]

#                 mysql.session.add(house)
#                 mysql.session.commit()

#                 response = {
#                     "status": "success",
#                     "house": {
#                         "id": house.id,
#                         "name": house.name,
#                         "rent": house.rent,
#                         "deposit": house.deposit,
#                         "floor": house.floor,
#                         "status": house.status,
#                         "apartment_id": house.apartment_id
#                     }
#                 }
#                 return make_response(jsonify(response)), 200
#     else:
#         response = {"status": "fail", "message": "Unauthorized Request"}
#         return make_response(jsonify(response)), 401

# @api.route('/api/v1/house/<int:id>', methods=['DELETE'])
# @login_required
# def delete_house(id):
#     data = get_user_details_from_header()
#     house = House.query.get(id)
#     if not house:
#         return make_response(jsonify({'status': 'fail', 'message': "Not found"})), 404
#     if data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         if caretaker.apartment_id == house.apartment_id:
#             if house.status:
#                 return make_response(jsonify({'status': 'fail', 'message': "Can't deleted occupied house"})), 406
#             mysql.session.delete(house)
#             mysql.session.commit()
            
#             return make_response(jsonify({'status': 'success'})), 204
            
    
#     return make_response(jsonify({'status': 'fail', 'message': "Forbidden request"})), 403

# @api.route('/api/v1/tenant/<int:id>/transaction', methods=['POST'])
# @login_required
# def add_transaction(id):
#     data = get_user_details_from_header()
#     tenant = Tenant.query.get(id)
#     if not tenant:
#         return make_response(jsonify({'status': 'fail', 'message': "Not found"})), 404
#     if data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         if caretaker.apartment_id == tenant.apartment_id:
            
#             post_data = request.get_json(force=True)
#             if not post_data:
#                 return make_response(jsonify({'status': 'fail', 'message': "Please provide all required fields"})), 409
#             else:
#                 if "transaction_id" not in post_data or "amount" not in post_data or "transaction_date" not in post_data or "transaction_image" not in post_data:
#                     return make_response(jsonify({'status': 'fail', 'message': "Please provide all required fields"})), 422

#                 transaction_id = post_data['transaction_id']
#                 amount = post_data['amount']
#                 transaction_date = post_data['transaction_date']
#                 transaction_image = post_data['transaction_image']

#                 transaction = TenantTransaction(transaction_id = transaction_id, amount = amount, transaction_date = transaction_date, tenant_id = tenant.id, timestamp = datetime.now(pytz.timezone('Africa/Nairobi')), transaction_image = transaction_image, apartment_id = tenant.apartment_id)
#                 tenant.amount = tenant.amount - amount
#                 mysql.session.add(tenant)
#                 mysql.session.add(transaction)
#                 mysql.session.commit()

#                 response = {
#                     "status": "success",
#                     "transaction": {
#                         "id": transaction.id,
#                         "transaction_id": transaction.transaction_id,
#                         "tenant_id": transaction.tenant_id,
#                         "amount": transaction.amount,
#                         "transaction_date": transaction.transaction_date,
#                         "transaction_image": transaction.transaction_image,
#                         "timestamp": transaction.timestamp
#                     }
#                 }
#                 return make_response(jsonify(response)), 200
    
#         response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#         return make_response(jsonify(response)), 401

# @api.route('/api/v1/tenant/<int:id>/transactions')
# @login_required
# def get_tenant_transaction(id):
#     data = get_user_details_from_header()
#     tenant = Tenant.query.get(id)
#     if not tenant:
#         return make_response(jsonify({'status': 'fail', 'message': "Not found"})), 404
#     if data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         if caretaker.apartment_id == tenant.apartment_id:
#             transactions = mysql.session.query(TenantTransaction).filter_by(tenant_id = tenant.id).with_entities(TenantTransaction.id, TenantTransaction.transaction_id, TenantTransaction.amount, TenantTransaction.transaction_date, TenantTransaction.transaction_image, TenantTransaction.tenant_id, TenantTransaction.timestamp).all()
#             transactions = [dict(zip(x.keys(), x)) for x in transactions]
#             response = {
#                 "status": "success",
#                 "transactions": transactions
#             }
#             return make_response(jsonify(response)), 200
    
#     response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#     return make_response(jsonify(response)), 401

# @api.route('/api/v1/transactions')
# @login_required
# def get_all_transactions():
#     data = get_user_details_from_header()
#     if data["user"] == "supervisor":
#         supervisor = Supervisor.query.get(data["id"])
#         transactions = TenantTransaction.query.filter_by(apartment_id = supervisor.apartment_id).with_entities(TenantTransaction.id, TenantTransaction.transaction_id, TenantTransaction.amount, TenantTransaction.transaction_date, TenantTransaction.transaction_image, TenantTransaction.tenant_id).all()
#         transactions = [dict(zip(row.keys(), row)) for row in transactions]
#         response = {"status":"success", "transactions": transactions}

#     elif data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         transactions = TenantTransaction.query.filter_by(apartment_id = caretaker.apartment_id).with_entities(TenantTransaction.id, TenantTransaction.transaction_id, TenantTransaction.amount, TenantTransaction.transaction_date, TenantTransaction.transaction_image, TenantTransaction.tenant_id).all()
#         transactions = [dict(zip(row.keys(), row)) for row in transactions]
#         response = {"status":"success", "transactions": transactions}
#     else:
#         response = {"status": "fail", "message": "Unauthorized Request"}
#     return make_response(jsonify(response)), 200

# @api.route('/api/v1/transactions/<int:year>')
# @login_required
# def get_year_transactions(year):
#     data = get_user_details_from_header()
#     start_date = datetime(year, 1, 1)
#     end_date = datetime(year, 12, calendar.monthrange(year, 12)[1])
#     if data["user"] == "supervisor":
#         supervisor = Supervisor.query.get(data["id"])
#         transactions = TenantTransaction.query.filter_by(apartment_id = supervisor.apartment_id).filter(TenantTransaction.transaction_date >= start_date).filter(TenantTransaction.transaction_date >= end_date).with_entities(TenantTransaction.id, TenantTransaction.transaction_id, TenantTransaction.amount, TenantTransaction.transaction_date, TenantTransaction.transaction_image, TenantTransaction.tenant_id).all()
#         transactions = [dict(zip(row.keys(), row)) for row in transactions]
#         response = {"status":"success", "transactions": transactions}
#         return make_response(jsonify(response)), 200

#     elif data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         transactions = TenantTransaction.query.filter_by(apartment_id = caretaker.apartment_id).filter(TenantTransaction.transaction_date >= start_date).filter(TenantTransaction.transaction_date <= end_date).with_entities(TenantTransaction.id, TenantTransaction.transaction_id, TenantTransaction.amount, TenantTransaction.transaction_date, TenantTransaction.transaction_image, TenantTransaction.tenant_id).all()
#         transactions = [dict(zip(row.keys(), row)) for row in transactions]
#         response = {"status":"success", "transactions": transactions}
#         return make_response(jsonify(response)), 200
#     else:
#         response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#         return make_response(jsonify(response)), 401

# @api.route('/api/v1/transactions/<int:year>/<int:month>')
# @login_required
# def get_transactions(year, month):
#     data = get_user_details_from_header()
#     start_date = datetime(year, month, 1)
#     end_date = datetime(year, month, calendar.monthrange(year, month)[1])
#     if data["user"] == "supervisor":
#         supervisor = Supervisor.query.get(data["id"])
#         transactions = TenantTransaction.query.filter_by(apartment_id = supervisor.apartment_id).filter(TenantTransaction.transaction_date >= start_date).filter(TenantTransaction.transaction_date >= end_date).with_entities(TenantTransaction.id, TenantTransaction.transaction_id, TenantTransaction.amount, TenantTransaction.transaction_date, TenantTransaction.transaction_image, TenantTransaction.tenant_id).all()
#         transactions = [dict(zip(row.keys(), row)) for row in transactions]
#         response = {"status":"success", "transactions": transactions}
#         return make_response(jsonify(response)), 200

#     elif data["user"] == "caretaker":
#         caretaker = Caretaker.query.get(data["id"])
#         transactions = TenantTransaction.query.filter_by(apartment_id = caretaker.apartment_id).filter(TenantTransaction.transaction_date >= start_date).filter(TenantTransaction.transaction_date <= end_date).with_entities(TenantTransaction.id, TenantTransaction.transaction_id, TenantTransaction.amount, TenantTransaction.transaction_date, TenantTransaction.transaction_image, TenantTransaction.tenant_id).all()
#         transactions = [dict(zip(row.keys(), row)) for row in transactions]
#         response = {"status":"success", "transactions": transactions}
#         return make_response(jsonify(response)), 200
#     else:
#         response = {"status": "fail","message": "Type of user not right. Try again with valid fields."}
#         return make_response(jsonify(response)), 401

# def get_user_details_from_header():
#     token = request.headers["Authorization"].split(' ')[1]  
#     return Caretaker.decode_auth_token(token)