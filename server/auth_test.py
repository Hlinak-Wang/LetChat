#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Angeline
"""

from server.auth_functions import login, logout, register, reset_request, reset, generateToken, generate_handle_str
from server.user_class import User
from server.Data_class import Data
import hashlib
SECRET = 'IE4'


def clearData():
    data = Data()
    return data

def testData():
    data = Data()
    user = User("hello", "goodbye", "hi@gmail.com", hashlib.sha256("123456".encode("utf-8")).hexdigest(), "hellogoodbye", "dummytoken", 1)
    data.add_user(user)
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
    assert data.get_all_user_detail() ==  [{
        'u_id': 0,
        'email': "hi@gmail.com",
        'name_first': "hello",
        'name_last': "goodbye",
        'handle_str': "hellogoodbye",
        'profile_img_url': 'http://127.0.0.1:1024/static/default.jpg'
    }]
    user = data.get_user('u_id', 0)
    assert user.password == hashlib.sha256("123456".encode("utf-8")).hexdigest()
    assert user.permission_id == 1

    email = "good@gmail.com"
    password = "9876543"
    name_first = "hellohowareyou"
    name_last = "imfinethankyou"

    register_output = register(data, email, password, name_first, name_last)
    check_token_2 = generateToken(name_first, name_last)

    assert register_output['u_id'] == 1
    assert register_output['token'] == check_token_2
    assert data.get_all_user_detail() == [{
        'u_id': 0,
        'email': "hi@gmail.com",
        'name_first': "hello",
        'name_last': "goodbye",
        'handle_str': "hellogoodbye",
        'profile_img_url': 'http://127.0.0.1:1024/static/default.jpg'
    }, {
        'u_id': 1,
        'email': "good@gmail.com",
        'name_first': "hellohowareyou",
        'name_last': "imfinethankyou",
        'handle_str': "hellohowareyouimfine",
        'profile_img_url': 'http://127.0.0.1:1024/static/default.jpg'
    }]
    user = data.get_user('u_id', 1)
    assert user.password == hashlib.sha256("9876543".encode("utf-8")).hexdigest()
    assert user.permission_id == 3

# below is a test to check what happens when a handle is already in use
def test_auth_register_handle():
    data = testData()

    email = "bye@gmail.com"
    password = "123456"
    name_first = "hello"
    name_last = "goodbye"

    register_output = register(data, email, password, name_first, name_last)
    #check_token = generateToken(name_first, name_last)
    check_handle = generate_handle_str(data, name_first, name_last)
    user = data.get_user('u_id', 1)
    assert user.handle_str == check_handle

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
    assert data.get_all_user_detail() == [{
            'u_id': 0,
            'email': "hi@gmail.com",
            'name_first': "hello",
            'name_last': "goodbye",
            'handle_str': "hellogoodbye",
            'profile_img_url': 'http://127.0.0.1:1024/static/default.jpg'
    }]
    user = data.get_user('u_id', 0)
    assert user.token == None

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

def test_passwordreset():
    data = testData()
    code = reset_request(data, 'hi@gmail.com')
    # Assume the reset request is sent

    # Invalid test
    assert reset(data, code, '') == {'ValueError': "This password is too short"}

    assert reset(data, 'asdf', '1234561') == {'ValueError': "This is not a valid reset code"}

    # Valid test
    output = reset(data, code, 'abcdsdg')
    assert output == {}

    is_success = login(data, 'hi@gmail.com', 'abcdsdg')
    assert is_success['u_id'] == 0
