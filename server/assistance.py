from datetime import datetime
import re


def check_valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(regex, email):
        return {'ValueError': "This email is not valid"}


def check_user_details(data, email, password):

    for user in data['users']:
        if user['email'] == email:
            if user['password'] == password:
                return user
            else:
                return {'ValueError': "Incorrect password entered"}

    return {'ValueError': "This email does not belong to a user"}


def check_valid_password(password):
    if len(password) < 6:
        return {'ValueError': "This password is too short"}


def check_already_user(data, email):
    for user in data['users']:
        if user['email'] == email:
            return {'ValueError': "This email is already in use by a user"}


def check_name(name_first, name_last):

    if len(name_first) < 1 or len(name_last) < 1:
        return {'ValueError': "First name or last name too short"}

    elif len(name_first) > 50 or len(name_last) > 50:
        return {'ValueError': "First name or last name too long"}


def handleAlreadyExists(data, handle):
    for user in data['users']:
        if user['handle_str'] == handle:
            return True
    return False


def findUserFromToken(data, token):
    for user in data['users']:
        if user['token'] == token:
            return user

    return None


def findUserFromEmail(data, email):

    for user in data['users']:
        if user['email'] == email:
            return user

    return None
