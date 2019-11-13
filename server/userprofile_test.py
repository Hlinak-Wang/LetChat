#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Yimeng
"""

from server.user_function import usersetemail, usersetname, usersethandle, getprofile, useruploadphoto
from server.auth_functions import register
from server.Data_class import Data

#fet global data
data = Data()
#test getproflie
def test_profile():
    global data
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
    global data
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
    profile = getprofile(data, auth_key["token"], auth_key["u_id"])[0]
    assert profile["name_first"] == first_short
    assert profile["name_last"] == last_short

#test setemail
def test_setemail():
    global data
    # Register two user for testing
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')
    register(data, 'email@gmail.com1', 'password1', 'name_first1', 'name_last1')

    invalid_email = 'dffgfddfsa.com'
    email_used_already = 'email@gmail.com'

    # Invalid input
    wrongmessage = usersetemail(data, None, invalid_email)[1]
    assert wrongmessage == "token doesn't exit"

    wrongmessage = usersetemail(data, auth_key["token"], invalid_email)[1]
    assert wrongmessage == 'Email entered is not a valid email'

    wrongmessage = usersetemail(data, auth_key["token"], email_used_already)[1]
    assert wrongmessage == 'Email address is already being used by another user'

    wrongmessage = usersetemail(data, 'token_not_registed', '123@gmail.com')[1]
    assert wrongmessage == 'User with token is not a valid user'

    # Valid input
    usersetemail(data, auth_key["token"], 'newemail@gmail.com')
    profile = getprofile(data, auth_key["token"], auth_key["u_id"])[0]
    assert profile["email"] == 'newemail@gmail.com'


# test sethanle
def test_sethandle():
    global data
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
    usersethandle(data, user["token"], 'testing')
    profile, error = getprofile(data, user["token"], user["u_id"])
    assert profile["handle_str"] == 'testing'

def test_useruploadphoto():

    # Invalid input
    assert useruploadphoto('token', 'https://webpagecannotopen.com/', 20, 20, 500, 377) == "img_url is returns an HTTP status other than 200."

    assert useruploadphoto('token', 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3541279145,3369708817&fm=26&gp=0.jpg',\
     -1, -1, 500, 377) == "img_url is returns an HTTP status other than 200."

    assert useruploadphoto('token', 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3541279145,3369708817&fm=26&gp=0.jpg',\
     0, 0, 9999, 9999) == "img_url is returns an HTTP status other than 200."

    assert useruploadphoto('token', 'https://www.google.com.hk/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png',\
     20, 20, 50, 37) == "Image uploaded is not a JPG"

    # Valid input
    useruploadphoto('token', 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3541279145,3369708817&fm=26&gp=0.jpg', 20, 20, 500, 377)
    
