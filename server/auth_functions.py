#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Angeline
"""

import hashlib
import jwt
from datetime import datetime
from server.user_class import User
from server.helper import (
        check_name,
        check_valid_password,
        check_valid_email,
        authorise,
        user_login_verify
)
# HELPER FUNCTIONS BELOW

SECRET = 'IE4'


def generateToken(email):
    payload = {
        'email': email,
        'time_create': datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
    }
    return str(jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8'))


def generate_handle_str(data, first, last, email):
    handle_str = first + last
    excess = len(handle_str) - 20
    if excess > 0:
        handle_str = handle_str[:20]

    if (data.get_element('users_group', 'handle_str', handle_str) is not None)\
            or (len(handle_str) < 3):
        handle_str = email

    return handle_str

# HELPER FUNCTIONS ABOVE


def login(data, email, password):
    email_check = check_valid_email(email)

    user = user_login_verify(data, email, password)

    if 'ValueError' in email_check:
        return email_check

    if type(user) == dict and 'ValueError' in user:
        return user

    token = generateToken(user.email)

    user.login(token)

    return {'u_id': user.u_id, 'token': user.token}


@authorise
def logout(data, user):

    if user.token is not None:
        user.logout()
        is_success = True
    else:
        is_success = False

    return {'is_sucess': is_success}


def register(data, email, password, name_first, name_last, host):
    email_check = check_valid_email(email)

    password_check = check_valid_password(password)

    name_check = check_name(name_first, name_last)
    # check if the user already exists
    unique = data.check_unique('users_group', 'email', email)
    if 'ValueError' in email_check:
        return email_check

    if 'ValueError' in password_check:
        return password_check

    if 'ValueError' in name_check:
        return name_check

    if not unique:
        return {'ValueError': "This email is already in use by a registered \
user"}

    token = generateToken(email)

    handle_str = generate_handle_str(data, name_first, name_last, email)

    password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    if len(data.users_group) == 0:
        permission_id = 1
    else:
        permission_id = 3

    new_user = User(name_first, name_last, email, password, handle_str, token,
                    permission_id, host)

    data.add_user(new_user)

    return {'u_id': new_user.u_id, 'token': new_user.token}


def reset_request(data, email):
    user = data.get_element('users_group', 'email', email)

    if user is None:
        return {'ValueError': "This email does not belong to a registered \
user"}

    code = jwt.encode({'email': email}, SECRET, algorithm='HS256').decode('utf-8')
    user.password_code(code)

    return user.reset_code


def reset(data, reset_code, new_password):

    password_check = check_valid_password(new_password)

    if 'ValueError' in password_check:
        return password_check

    user = data.get_element('users_group', 'reset_code', reset_code)

    if user is None:
        return {'ValueError': "This is not a valid reset code"}

    new_password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()

    user.reset_password(new_password)

    return {}
