#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Yimeng
"""

from server.user_function import usersetemail, usersetname, usersethandle, getprofile, useruploadphoto
from server.auth_functions import register
from server.Data_class import Data


# fet global data
data = Data()
host = 'http://127.0.0.1:5555/'


# test getproflie
def test_profile():
    global data, host
    # Create one user for testing
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last', host)

    # Invalid input
    result = getprofile(data, None, None, host)
    assert result == {'ValueError': "token not valid"}

    result = getprofile(data, auth_key['token'], 'not_valid_u_id', host)
    assert result == {'ValueError': "User with u_id is not a valid user"}

    # Valid input
    result = getprofile(data, auth_key["token"], auth_key["u_id"], host)
    assert result["email"] == 'email@gmail.com'
    assert result["name_first"] == 'name_first'
    assert result["name_last"] == 'name_last'
    # Assume the default handle is the first_namelast_name
    assert result["handle_str"] == 'name_firstname_last'


def test_get_all_user():
    global data
    user_list = data.get_all_user_detail(host)
    assert len(user_list) == 1
    assert user_list[0]['name_first'] == 'name_first'
    assert user_list[0]['name_last'] == 'name_last'
    assert user_list[0]['email'] == 'email@gmail.com'


# test setname
def test_setname():
    global data, host
    data = Data()
    # create one user
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last', host)

    # name_first more than 50 characters but not name_last
    first_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    first_short = 'asdfzxcv'

    last_short = 'abcd'
    last_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    # Invalid input
    result = usersetname(data, None, first_long, last_short)
    assert result == {'ValueError': "token not valid"}

    result = usersetname(data, auth_key["token"], first_long, last_short)
    assert result == {'ValueError': 'name_first is not between 1 and 50 characters in length'}

    result = usersetname(data, auth_key["token"], first_short, last_long)
    assert result == {'ValueError': 'name_last is not between 1 and 50 characters in length'}

    result = usersetname(data, 'token_not_registed', first_short, last_short)
    assert result == {'ValueError': 'token not valid'}

    # Valid input
    usersetname(data, auth_key["token"], first_short, last_short)
    result = getprofile(data, auth_key["token"], auth_key["u_id"], host)
    assert result["name_first"] == first_short
    assert result["name_last"] == last_short


# test setemail
def test_setemail():
    global data, host
    data = Data()
    # Register two user for testing
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last', host)
    register(data, 'email@gmail.com1', 'password1', 'name_first1', 'name_last1', host)

    invalid_email = 'dffgfddfsa.com'
    email_used_already = 'email@gmail.com'

    # Invalid input
    result = usersetemail(data, None, invalid_email)
    assert result == {'ValueError': "token not valid"}

    result = usersetemail(data, auth_key["token"], invalid_email)
    assert result == {'ValueError': 'Email entered is not a valid email'}

    result = usersetemail(data, auth_key["token"], email_used_already)
    assert result == {'ValueError': 'Email address is already being used by another user'}

    result = usersetemail(data, 'token_not_registed', '123@gmail.com')
    assert result == {'ValueError': 'token not valid'}

    # Valid input
    usersetemail(data, auth_key["token"], 'newemail@gmail.com')
    result = getprofile(data, auth_key["token"], auth_key["u_id"], host)
    assert result["email"] == 'newemail@gmail.com'


# test sethanle
def test_sethandle():
    global data, host
    data = Data()
    user = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last', 'http://127.0.0.1:5555/')
    other_user = register(data, 'other@gmail.com', 'password', 'first', 'last', 'http://127.0.0.1:5555/')

    handle_long = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
    handle_normal = 'normal'

    handle_used = 'handle_str'
    usersethandle(data, other_user['token'], handle_used)

    # Invalid input
    # handle_str is no more than 20 charaters
    result = usersethandle(data, None, handle_normal)
    assert result == {'ValueError': "token not valid"}

    result = usersethandle(data, user["token"], handle_long)
    assert result == {'ValueError': "handle_str must be between 3 and 20"}

    result = usersethandle(data, user["token"], handle_used)
    assert result == {'ValueError': "handle is already used by another user"}

    result = usersethandle(data, 'token_not_registed', handle_normal)
    assert result == {'ValueError': 'token not valid'}

    # Valid input
    usersethandle(data, user["token"], 'testing')
    result = getprofile(data, user["token"], user["u_id"], host)
    assert result["handle_str"] == 'testing'
    
    '''
def test_useruploadphoto():
    global data
    data = Data()

    user = register(data, 'email@gmail.com', 'password', '123456', '123456')
    # Invalid input
    assert useruploadphoto(data, user['token'], 'https://webpagecannotopen.com/', 20, 20, 500, 377) == {'ValueError': "img_url is returns an HTTP status other than 200."}

    assert useruploadphoto(data, user['token'], 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3541279145,3369708817&fm=26&gp=0.jpg', \
     -1, -1, 500, 377) == {'ValueError': "any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL."}

    assert useruploadphoto(data, user['token'], 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3541279145,3369708817&fm=26&gp=0.jpg', \
     0, 0, 9999, 9999) == {'ValueError': "any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL."}

    assert useruploadphoto(data, user['token'], 'https://www.google.com.hk/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png', \
     20, 20, 50, 37) == {'ValueError': "Image uploaded is not a JPG"}

    # Valid input
    assert useruploadphoto(data, user['token'], 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3541279145,3369708817&fm=26&gp=0.jpg', 20, 20, 500, 377) == {}

    assert useruploadphoto(data, user['token'], 'https://img-bbs.csdn.net/upload/201712/28/1514449450_50879.jpg', 20, 20, 500, 377) == {}
    '''