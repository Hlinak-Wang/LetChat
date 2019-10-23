from json import dumps
from flask import Flask, request
import re
import jwt
from datetime import datetime
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

#import functions from another file
def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)


#class Member:
#    def __init__(self, u_id, name_first, name_last)
    

#self.handle = first + last;

data = {
    "messages": {}, 
    "users": [],
    "channel_id": {},
}

SECRET = 'IE4';

#in user_data:
#{'u_id': u_id, 'name_first': name_first, "name_last": name_last, 'token': token, "handle": handle, 'email': email, 'password': password, 'permission_id': permission_id, 'channel_involve': [], 'reset_code': reset_code}

#def get_user_data():
#    global data
#    global SECRET
#    return data.get("user_data")
    #return specific type of data?

#HELPER FUNCTIONS BELOW



#FIX BELOW
class ValueError(HTTPException):
    code = 400
    message = 'No message specified'
#FIX ABOVE

def check_valid_email(email): 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(regex, email):  
        raise ValueError(description="This email is not valid")

def check_user_details(data, email, password):
    
    for user in data['users']:
        if user['email'] == email:
            if user['password'] == password:
                return user
            else:
                raise ValueError(description="Incorrect password entered")
                
    raise ValueError(description="This email does not belong to a user")
    

def check_valid_password(password):
    if len(password) < 6:
        raise ValueError(description="This password is too short")


def check_already_user(email):
    global data
    for user in data['users']:
        if user['email'] == email:
            raise ValueError(description="This email is already in use by a user")


def check_name(name_first, name_last):
    if ((len(name_first) < 1) or (len(name_last) < 1)):
        raise ValueError(description="First name or last name too short")
    elif (len(name_first) > 50 or (len(name_last) > 50)):
        raise ValueError(description="First name or last name too long")


def generateToken(first, last):
    payload = {
        'first': first,
        'last': last,
        'time_create': datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
    }
    return jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')

     
def generateHandle(first, last):
    global data
    handle = first + last
    excess = len(handle) - 20
    if excess > 0:
        handle = handle[:21]
    
    if (handleAlreadyExists(handle) or len(handle) < 3):
        handle = datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")

    return handle
                
def handleAlreadyExists(handle):
    global data
    for user in data['users']:
        if user['handle'] == handle:
            return True
    return False

def findUserFromToken(token):
    global data
    for user in data['users']:
        if user['token'] == token:
            return user

    return None

def findUserFromEmail(email):
    global data
    for user in data['users']:
        if user['email'] == email:
            return email

    return None

def decoding_reset_code(reset_code):
    return jwt.decode(reset_code, SECRET, algorithms=['HS256'])
    

#HELPER FUNCTIONS ABOVE

@APP.route("/auth/login", methods=['POST'])
def auth_login():
    # fn_auth_login(request.args.get('email'), request.form.get('password'))
    #return dumps({})
    
    global data
    print("hi")
    email = request.args.get('email')
    password = request.args.get('password')
    check_valid_email(email)
    user = check_user_details(data, email, password)
    
    token = generateToken(user['name_first'], user['name_last'])
    
    return dumps({'u_id': user['u_id'], 'token': token,
    })
    

@APP.route("/auth/logout", methods = ['POST']) #done?
def auth_logout():
    global data
    
    token = request.form.get('token')
    
    user = findUserFromToken(token)
    
    if user is not None:
        user['token'] = None
        is_success = True

    return dumps({
            'is_sucess': is_success
            })
    
@APP.route("/auth/register", methods=['POST'])  # done, not checked
def auth_register():
    global data
    print("hi")
    email = request.form.get('email')
    
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    check_valid_email(email)
    
    
    check_valid_password(password)
    
    check_name(name_first, name_last)
    
    
    check_already_user(email)
    
    u_id = len(data['users'])
    
    token = generateToken(name_first, name_last)
    
    handle = generateHandle(name_first, name_last)
    
    if u_id == 0:
        permission = 1
    else:
        permission = 3

    data['users'].append({
        'u_id': u_id,
        'name_first': name_first,
        'name_last': name_last,
        'token': token,
        'handle': handle,
        'email': email,
        'password': password,
        'permission_id': permission,
        'channel_involve': [],
        'reset_code': None,
    })
    print(data)
    user = check_user_details(data, email, password)
    print(user['email'])
    return dumps({
        'u_id': u_id,
        'token': token
    })


@APP.route("/auth/passwordreset/request", methods = ['POST'])
def auth_reset_request():
    global data
    email = request.form.get('email')
    user = findUserFromEmail(email)
    
    code = jwt.encode({'email': email}, SECRET, algorithm='HS256').decode('utf-8')
    #SEND AN EMAIL
    user['reset_code'] = code
    
    return dumps({})

@APP.route("/auth/passwordreset/reset", methods = ['POST'])
def auth_reset():
    global data
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    
    return_dictionary = decoding_reset_code(reset_code)
    email = return_dictionary['email']
    user = findUserFromEmail(email)
    
    if user == None:
        raise ValueError(description="This is not a valid reset code")
    
    check_valid_password(new_password)
    
    user['password'] = new_password
    
    user['reset_code'] = None
    
    
    return dumps({})


if __name__ == "__main__":
    APP.run(debug=True)
