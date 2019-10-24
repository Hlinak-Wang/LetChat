"""Flask server"""
import sys
import os
from json import dumps
from flask import Flask, request
import re
import jwt
from datetime import datetime
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from channel_function import (
    ch_create,
    ch_invite,
    ch_details,
    ch_leave,
    ch_join,
    ch_addowner,
    ch_removeowner,
    ch_lists,
    ch_listall,
    fun_channel_message,
    fun_send
)
import pickle


# import functions from another file
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

data = {
    "users": [],
    "channels": [],
    "message_counter": 0
}

#if os.path.getsize('/tmp_amd/glass/export/glass/4/z5261785/Desktop/COMP1531/test/save.dat') > 0:
 #   data = pickle.load(open('save.dat','rb'))

SECRET = 'IE4';

#FIX BELOW
class ValueError(HTTPException):
    code = 400
    message = 'No message specified'
class Exception(HTTPException):
    code = 400
    message = "No message specified"
class AccessError(HTTPException):
    code = 400
    message = "No message specified"
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
    

def save():
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)


@APP.route("/auth/login", methods=['POST'])
def auth_login():
    # fn_auth_login(request.args.get('email'), request.form.get('password'))
    #return dumps({})
    
    global data
    email = request.form.get('email')
    password = request.form.get('password')
    check_valid_email(email)
    user = check_user_details(data, email, password)
    
    token = generateToken(user['name_first'], user['name_last'])
    user['token'] = token
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)

    
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

    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
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
    user = check_user_details(data, email, password)
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps({
        'u_id': u_id,
        'token': token
    })


@APP.route('/channels/create', methods=['POST'])
def channel_create():
    global data
    token = request.form.get('token')
    channel_name = request.form.get('name')
    is_public = request.form.get('is_public')
    if is_public == "true":
        is_public = True
    else:
        is_public = False
    channel_id = ch_create(data, token, channel_name, is_public)
    if 'ValueError' in channel_id:
        raise ValueError(description=channel_id['ValueError'])
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(channel_id)


@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    global data
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    channel_id = request.form.get('channel_id')
    result = ch_invite(data, token, u_id, channel_id)
    if 'ValueError' in result:
        raise ValueError(description=result['ValueError'])
    elif 'Exception' in result:
        raise Exception(description=result['Exception'])
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps()


@APP.route('/channel/details', methods=['GET'])
def channel_details():
    global data
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    channel_detail = ch_details(data, token, channel_id)
    if 'ValueError' in channel_detail:
        raise ValueError(description=channel_detail['ValueError'])
    elif 'Exception' in channel_detail:
        raise Exception(description=channel_detail['Exception'])
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(channel_detail)


@APP.route('/channel/messages', methods=['GET'])
def channel_message():
    channel_id = int(request.args.get('channel_id'))
    token = request.args.get('token')
    start = int(request.args.get('start'))
    messages = fun_channel_message(data, token, channel_id, start)
    if 'ValueError' in messages:
        raise ValueError(description=messages['ValueError'])
    elif 'AccessError' in messages:
        raise Exception(description=messages['AccessError'])
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(messages)


@APP.route('/message/send', methods=['POST'])
def message_send():
    global data
    #send_message_buffer(data)
    message = request.form.get('message')
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    output = fun_send(data, token, channel_id, message)

    # save()
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    return dumps(output)


@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    global data
    channel_id = int(request.form.get('channel_id'))
    token = request.form.get('token')
    output = ch_leave(data, token, channel_id)
    if 'ValueError' in output:
       raise ValueError(description=output['ValueError'])
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(output)


@APP.route('/channel/join', methods=['POST'])
def channel_join():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    join = ch_join(data, token, channel_id)
    if 'ValueError' in join:
        raise ValueError(description=join['ValueError'])
    elif 'AccessError' in join:
        raise AccessError(description=join['AccessError'])
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(join)


@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    addowner = ch_addowner(data, token, channel_id, u_id)
    if 'ValueError' in addowner:
        raise ValueError(description=addowner['ValueError'])
    elif 'AccessError' in addowner:
        raise Exception(description=addowner['AccessError'])
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(addowner)


@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    removeowner = ch_removeowner(data, token, channel_id, u_id)
    if 'ValueError' in removeowner:
        raise ValueError(description=removeowner['ValueError'])
    elif 'AccessError' in removeowner:
        raise Exception(description=removeowner['AccessError'])
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(removeowner)


@APP.route('/channels/list', methods=['GET'])
def channel_list():
    global data
    token = request.args.get('token')
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(ch_lists(data, token))


@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    global data
    print(data)
    token = request.args.get('token')
    listall = ch_listall(data, token)
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)
    return dumps(listall)


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
