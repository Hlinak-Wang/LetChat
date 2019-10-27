#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Yimeng
"""

from server.user_function import usersetemail, usersetname, usersethandle, getprofile
from server.auth_functions import register

#fet global data
def getData():
    data = {
        'users': [],
        'channels': []
    }
    return data

#test getproflie
def test_profile():
    data = getData()
    # Create one user for testing
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')

    # Invalid input
    value, wrongmessage = getprofile(data, None, None)
    assert wrongmessage == "Invalid token or u_id"

    value, wrongmessage = getprofile(data, 'not_valid_token', 'not_valid_u_id')
    assert wrongmessage == "User with u_id is not a valid user"

    # Valid input
    value, wrongmessage = getprofile(data, auth_key["token"], auth_key["u_id"])
    assert value["email"] == 'email@gmail.com'
    assert value["name_first"] == 'name_first'
    assert value["name_last"] == 'name_last'
    # Assume the default handle is the first_namelast_name
    assert value["handle_str"] == 'name_firstname_last'

#test setname
def test_setname():
    data = getData()
    # create one user
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')

    # name_first more than 50 characters but not name_last
    first_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    first_short = 'asdfzxcv'

    last_short = 'abcd'
    last_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    # Invalid input
    value, wrongmessage = usersetname(data, None, first_long, last_short)
    assert wrongmessage == "token doesn't exit"

    value, wrongmessage = usersetname(data, auth_key["token"], first_long, last_short)
    assert wrongmessage == 'name_first is not between 1 and 50 characters in length'

    value, wrongmessage = usersetname(data, auth_key["token"], first_short, last_long)
    assert wrongmessage == 'name_last is not between 1 and 50 characters in length'

    value, wrongmessage = usersetname(data, 'token_not_registed', first_short, last_short)
    assert wrongmessage == 'User with token is not a valid user'

    # Valid input
    usersetname(data, auth_key["token"], first_short, last_short)
    profile, error = getprofile(data, auth_key["token"], auth_key["u_id"])
    assert profile["name_first"] == first_short
    assert profile["name_last"] == last_short

#test setemail
def test_setemail():
    data = getData()
    # Register two user for testing
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')
    auth_key1 = register(data, 'email@gmail.com1', 'password1', 'name_first1', 'name_last1')

    invalid_email = 'dffgfddfsa.com'
    email_used_already = 'email@gmail.com'

    # Invalid input
    value, wrongmessage = usersetemail(data, None, invalid_email)
    assert wrongmessage == "token doesn't exit"

    value, wrongmessage = usersetemail(data, auth_key["token"], invalid_email)
    assert wrongmessage == 'Email entered is not a valid email'

    value, wrongmessage = usersetemail(data, auth_key["token"], email_used_already)
    assert wrongmessage == 'Email address is already being used by another user'

    value, wrongmessage = usersetemail(data, 'token_not_registed', '123@gmail.com')
    assert wrongmessage == 'User with token is not a valid user'

    # Valid input
    value, wrongmessage = usersetemail(data, auth_key["token"], 'newemail@gmail.com')
    profile, error = getprofile(data, auth_key["token"], auth_key["u_id"])
    assert profile["email"] == 'newemail@gmail.com'

#test sethanle
def test_sethandle():
    data = getData()
    user = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')
    other_user = register(data, 'other@gmail.com', 'password', 'first', 'last')

    handle_long = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
    handle_normal = 'normal'

    handle_used = 'handle_str'
    usersethandle(data, other_user['token'], handle_used)

    # Invalid input
    # handle_str is no more than 20 charaters
    value, wrongmessage = usersethandle(data, None, handle_normal)
    assert wrongmessage == "token doesn't exit"

    value, wrongmessage = usersethandle(data, user["token"], handle_long)
    assert wrongmessage == "handle_str must be between 3 and 20"

    value, wrongmessage = usersethandle(data, user["token"], handle_used)
    assert wrongmessage == "handle is already used by another user"

    value, wrongmessage = usersethandle(data, 'token_not_registed', handle_normal)
    assert wrongmessage == "User with token is not a valid user"

    # Valid input
    value, wrongmessage = usersethandle(data, user["token"], 'testing')
    profile, error = getprofile(data, user["token"], user["u_id"])
    assert profile["handle_str"] == 'testing'

#test uploadphoto
def test_uploadphoto():
    # Create one user for testing
    pass
