from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask import Flask, request, jsonify
from json import dumps
import jwt
import sys
import re

# Make a regular expression
# for validating an Email
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


# Define a function for
# for validating an Email
def check(email):
    # pass the regualar expression
    # and the string in search() method
    if (re.search(regex, email)):
        return 1

    else:
        return 0

def getuser(data, token):

    for user in data['users']:
        if user['token'] == token:
            return user

    return None


def checkemailnotused(data, email):

    for user in data['users']:
        if user['email'] == email:
            return 0

    return 1


def checkhandlenotused(data, handle):

    for user in data['users']:
        if user['handle_str'] == handle:
            return 0

    return 1


def getprofile(data, token, u_id):
    value = None
    Errormessage = None

    if token == None or u_id == None:
        Errormessage = "Invalid token or u_id"
        return (value, Errormessage)

    user = getuser(data, token)

    if user == None:
        Errormessage = "User with u_id is not a valid user"
        return (value, Errormessage)

    value = {'email': user['email'],
             'name_first': user['name_first'],
             'name_last': user['name_last'],
             'handle_str': user['handle_str'], }

    return (value, Errormessage)


def usersetname(data, token, name_first, name_last):
    value = None
    Errormessage = None

    if token == None:
        Errormessage = "token doesn't exit"
        return (value, Errormessage)

    if len(name_first) > 50 or len(name_first) < 0:
        Errormessage = "name_first is not between 1 and 50 characters in length"
        return (value, Errormessage)

    if len(name_last) > 50 or len(name_last) < 0:
        Errormessage = "name_last is not between 1 and 50 characters in length"
        return (value, Errormessage)

    user = getuser(data, token)

    if user == None:
        Errormessage = "User with token is not a valid user"
        return (value, Errormessage)

    user['name_first'] = name_first
    user['name_last'] = name_last

    print(user)
    value = 1

    return (value, Errormessage)


def usersetemail(data, token, email):
    value = None
    Errormessage = None

    if token == None:
        Errormessage = "token doesn't exit"
        return (value, Errormessage)

    if check(email) == 0:
        Errormessage = "Email entered is not a valid email"
        return (value, Errormessage)

    if checkemailnotused(data, email) == 0:
        Errormessage = "Email address is already being used by another user"
        return (value, Errormessage)

    user = getuser(data, token)

    if user == None:
        Errormessage = "User with token is not a valid user"
        return (value, Errormessage)

    user['email'] = email

    value = 1

    return (value, Errormessage)


def usersethandle(data, token, handle_str):
    value = None
    Errormessage = None

    if token == None:
        Errormessage = "token doesn't exit"
        return (value, Errormessage)

    if len(handle_str) > 20 or len(handle_str) < 3:
        Errormessage = "handle_str must be between 3 and 20"
        return (value, Errormessage)

    if checkhandlenotused(data, handle_str) == 0:
        Errormessage = "handle is already used by another user"
        return (value, Errormessage)

    user = getuser(data, token)

    if user == None:
        Errormessage = "User with token is not a valid user"
        return (value, Errormessage)

    user['handle_str'] = handle_str

    value = 1

    return (value, Errormessage)
