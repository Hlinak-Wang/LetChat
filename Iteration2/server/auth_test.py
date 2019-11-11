#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Angeline
"""

from server.auth_functions import login, logout, register, reset_request, reset, generateToken, generateHandle
import hashlib
SECRET = 'IE4'


def clearData():
    data = {
        "messages": {},
        "users": [],
        "channel_id": {},
    }
    return data


def testData():
    data = {
        "messages": {},
        "users": [
            {
                'u_id': 0,
                'name_first': "hello",
                'name_last': "goodbye",
                'token': "dummytoken",
                'handle_str': "hellogoodbye",
                'email': "hi@gmail.com",
                'password': hashlib.sha256("123456".encode("utf-8")).hexdigest(),
                'permission_id': 1,
                'channel_involve': [],
                'reset_code': None
            }
        ],
        "channel_id": {},
    }

    return data


# START TEST AUTH_REGISTER
def test_auth_register_valid():
    data = clearData()

    email = "hi@gmail.com"
    password = "123456"
    name_first = "hello"
    name_last = "goodbye"

    register_output = register(data, email, password, name_first, name_last)
    check_token_1 = generateToken(name_first, name_last)

    assert register_output['u_id'] == 0
    assert register_output['token'] == check_token_1
    assert data['users'] == [{
        'u_id': 0,
        'name_first': "hello",
        'name_last': "goodbye",
        'token': check_token_1,
        'handle_str': "hellogoodbye",
        'email': "hi@gmail.com",
        'password': hashlib.sha256("123456".encode("utf-8")).hexdigest(),
        'permission_id': 1,
        'channel_involve': [],
        'reset_code': None
    }]

    email = "good@gmail.com"
    password = "9876543"
    name_first = "hellohowareyou"
    name_last = "imfinethankyou"

    register_output = register(data, email, password, name_first, name_last)
    check_token_2 = generateToken(name_first, name_last)

    assert register_output['u_id'] == 1
    assert register_output['token'] == check_token_2
    assert data['users'] == [{
        'u_id': 0,
        'name_first': "hello",
        'name_last': "goodbye",
        'token': check_token_1,
        'handle_str': "hellogoodbye",
        'email': "hi@gmail.com",
        'password': hashlib.sha256("123456".encode("utf-8")).hexdigest(),
        'permission_id': 1,
        'channel_involve': [],
        'reset_code': None
    }, {
        'u_id': 1,
        'name_first': "hellohowareyou",
        'name_last': "imfinethankyou",
        'token': check_token_2,
        'handle_str': "hellohowareyouimfine",
        'email': "good@gmail.com",
        'password': hashlib.sha256("9876543".encode("utf-8")).hexdigest(),
        'permission_id': 3,
        'channel_involve': [],
        'reset_code': None
    }]


# below is a test to check what happens when a handle is already in use
def test_auth_register_handle():
    data = testData()

    email = "bye@gmail.com"
    password = "123456"
    name_first = "hello"
    name_last = "goodbye"

    register_output = register(data, email, password, name_first, name_last)
    check_token = generateToken(name_first, name_last)
    check_handle = generateHandle(data, name_first, name_last)

    assert data['users'] == [{
        'u_id': 0,
        'name_first': "hello",
        'name_last': "goodbye",
        'token': "dummytoken",
        'handle_str': "hellogoodbye",
        'email': "hi@gmail.com",
        'password': hashlib.sha256("123456".encode("utf-8")).hexdigest(),
        'permission_id': 1,
        'channel_involve': [],
        'reset_code': None
    }, {
        'u_id': 1,
        'name_first': "hello",
        'name_last': "goodbye",
        'token': check_token,
        'handle_str': check_handle,
        'email': "bye@gmail.com",
        'password': hashlib.sha256("123456".encode("utf-8")).hexdigest(),
        'permission_id': 3,
        'channel_involve': [],
        'reset_code': None
    }]


def test_auth_register_invalid_email():
    data = clearData()

    email = "hi"
    password = "123456"
    name_first = "hello"
    name_last = "goodbye"

    register_output = register(data, email, password, name_first, name_last)
    assert register_output == {'ValueError': "This email is not valid"}


def test_auth_register_invalid_password():
    data = clearData()

    email = "hi@gmail.com"
    password = "123"
    name_first = "hello"
    name_last = "goodbye"

    register_output = register(data, email, password, name_first, name_last)
    assert register_output == {'ValueError': "This password is too short"}


def test_auth_register_invalid_name():
    data = clearData()

    email = "hi@gmail.com"
    password = "123456"
    name_first = ""
    name_last = ""

    register_output = register(data, email, password, name_first, name_last)
    assert register_output == {'ValueError': "First name or last name too short"}

    data = clearData()

    name_first = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    name_last = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    register_output = register(data, email, password, name_first, name_last)
    assert register_output == {'ValueError': "First name or last name too long"}


def test_auth_register_already_user():
    data = testData()

    email = "hi@gmail.com"
    password = "123456"
    name_first = "hello"
    name_last = "goodbye"

    register_output = register(data, email, password, name_first, name_last)

    assert register_output == {'ValueError': "This email is already in use by a user"}


# END TEST AUTH_REGISTER

# START TEST AUTH_LOGIN

def test_auth_login_valid():
    data = testData()

    email = "hi@gmail.com"
    password = "123456"
    name_first = "hello"
    name_last = "goodbye"

    check_token = generateToken(name_first, name_last)
    login_output = login(data, email, password)

    assert login_output == {'u_id': 0, 'token': check_token}


def test_auth_login_invalid_email():
    data = testData()

    email = "hi"
    password = "123456"

    login_output = login(data, email, password)
    assert login_output == {'ValueError': "This email is not valid"}


def test_auth_login_invalid_user():
    # wrong password
    data = testData()

    email = "hi@gmail.com"
    password = "1234567"

    login_output = login(data, email, password)
    assert login_output == {'ValueError': "Incorrect password entered"}

    # wrong email
    data = testData()

    email = "hello@gmail.com"
    password = "123456"

    login_output = login(data, email, password)
    assert login_output == {'ValueError': "This email does not belong to a user"}


# END TEST AUTH_LOGIN

# START TEST AUTH_LOGOUT
def test_auth_logout_valid():
    data = testData()
    token = "dummytoken"
    logout_output = logout(data, token)

    assert logout_output == {'is_sucess': True}
    assert data['users'] == [
        {
            'u_id': 0,
            'name_first': "hello",
            'name_last': "goodbye",
            'token': None,
            'handle_str': "hellogoodbye",
            'email': "hi@gmail.com",
            'password': hashlib.sha256("123456".encode("utf-8")).hexdigest(),
            'permission_id': 1,
            'channel_involve': [],
            'reset_code': None
        }]


def test_auth_logout_invalid_token():
    data = testData()
    token = "incorrect"
    logout_output = logout(data, token)
    assert logout_output == {'is_sucess': False}


# END TEST AUTH_LOGOUT

# START TEST AUTH_PASSWORDRESET_REQUEST

# We can be sure that this function has worked correctly if we receive an email with a reset code, and no exceptions have been thrown.

# END TEST AUTH_PASSWORDRESET_REQUEST

# START TEST AUTH_PASSWORDRESET_RESET

def test_passworldreset():
    data = testData()
    code = reset_request(data, 'hi@gmail.com')
    # Assume the reset request is sent

    # Invalid test
    assert reset(data, code, '') == {
        'ValueError': "This password is too short"
    }

    assert reset(data, 'asdf', '1234561') == {
        'ValueError': "This is not a valid reset code"
    }

    # Valid test
    output = reset(data, code, 'abcdsdg')
    assert output == {}

    is_success = login(data, 'hi@gmail.com', 'abcdsdg')
    assert is_success['u_id'] == 0