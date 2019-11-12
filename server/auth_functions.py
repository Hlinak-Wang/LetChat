#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Angeline
"""

import re
import hashlib
import jwt
from datetime import datetime
import server.Data_class
from server.user_class import User

# HELPER FUNCTIONS BELOW

SECRET = 'IE4'

def check_valid_email(email):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if not re.search(regex, email):
        return {'ValueError': "This email is not valid"}
    return {}

def check_valid_password(password):
    if len(password) < 6:
        return {'ValueError': "This password is too short"}
    return {}

def check_name(name_first, name_last):
    if (len(name_first) < 1) or (len(name_last) < 1):
        return {'ValueError': "First name or last name too short"}
    elif len(name_first) > 50 or (len(name_last) > 50):
        return {'ValueError': "First name or last name too long"}

    return {}

def generateToken(first, last):
    payload = {
        'first': first,
        'last': last,
        'time_create': datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
    }
    return str(jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8'))


def generate_handle_str(data, first, last):
    handle_str = first + last
    excess = len(handle_str) - 20
    if excess > 0:
        handle_str = handle_str[:20]

    if (data.get_user('handle_str', handle_str) is not None) or (len(handle_str) < 3):
        handle_str = datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")

    return handle_str

def decoding_reset_code(reset_code):
    return jwt.decode(reset_code, SECRET, algorithms=['HS256'])


# HELPER FUNCTIONS ABOVE

def login(data, email, password):
    email_check = check_valid_email(email)
    
    user = data.user_login_verify(email, password)
    
    if 'ValueError' in email_check:
        return email_check

    if type(user) == dict and 'ValueError' in user:
        return user
    
    token = generateToken(user.name_first, user.name_last)
    
    user.login(token)

    return {'u_id': user.u_id, 'token': user.token}


def logout(data, token):
    user = data.get_user('token', token)
    
    if user is not None:
        user.logout()
        is_success = True
    else:
        is_success = False
        
    return {'is_sucess': is_success}


def register(data, email, password, name_first, name_last):
    email_check = check_valid_email(email)
    
    password_check = check_valid_password(password)
    
    name_check = check_name(name_first, name_last)
    
    unique = data.check_unique('email', email) #check if the user already exists

    if 'ValueError' in email_check:
        return email_check

    if 'ValueError' in password_check:
        return password_check

    if 'ValueError' in name_check:
        return name_check

    if not unique:
        return {'ValueError': "This email is already in use by a registered user"}

    token = generateToken(name_first, name_last)

    handle_str = generate_handle_str(data, name_first, name_last)
    
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    if data.get_user_number() == 0:
        permission_id = 1
    else:
        permission_id = 3
    
    new_user = User(name_first, name_last, email, password, handle_str, token, permission_id)
    
    data.add_user(new_user)

    return {'u_id': new_user.u_id, 'token': new_user.token}


def reset_request(data, email):
    user = data.get_user('email', email)
    
    if user is None:
        return {'ValueError': "This email does not belong to a registered user"}

    code = jwt.encode({'email': email}, SECRET, algorithm='HS256').decode('utf-8')
    user.password_code(code)

    return user.reset_code


def reset(data, reset_code, new_password):
    user = data.get_user('reset_code', reset_code)

    if user is None:
        return {'ValueError': "This is not a valid reset code"}

    password_check = check_valid_password(new_password)
    
    if 'ValueError' in password_check:
        return password_check
    
    new_password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
    
    user.reset_password(new_password)

    return {}
