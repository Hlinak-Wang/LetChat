#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Yimeng
"""
import sys
import re
import urllib.request
import requests
from PIL import Image

'''
def getHttpStatusCode(url):
    try:

        request = requests.get(url)

        httpStatusCode = request.status_code

        return httpStatusCode

    except requests.exceptions.HTTPError as e:

        return e

'''
# Make a regular expression

# Define a function for
# for validating an Email
def check(email):
    # pass the regualar expression
    Regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # and the string in search() method
    if re.search(Regex, email):
        return 1
    return 0


# get user profile by token
def getprofile(data, token, u_id):
    value = None
    wrongmessage = None

    if token is None or u_id is None:
        wrongmessage = "Invalid token or u_id"
        return value, wrongmessage

    user = data.get_user('token', token)

    if user is None:
        wrongmessage = "User with u_id is not a valid user"
        return value, wrongmessage

    value = user.get_user_detail()
    return value, wrongmessage


def get_all_users(data, token):
    value = None
    wrongmessage = None
    if data.get_user('token', token) is None:
        wrongmessage = 'Invalid token'

    user_list = data.get_all_user_detail()
    value = {
        'users': user_list
    }

    return value, wrongmessage
    

# set username by token
def usersetname(data, token, name_first, name_last):
    value = None
    wrongmessage = None

    if token is None:
        wrongmessage = "token doesn't exit"
        return value, wrongmessage

    if len(name_first) > 50 or len(name_first) < 0:
        wrongmessage = "name_first is not between 1 and 50 characters in length"
        return value, wrongmessage

    if len(name_last) > 50 or len(name_last) < 0:
        wrongmessage = "name_last is not between 1 and 50 characters in length"
        return value, wrongmessage

    user = data.get_user('token', token)

    if user is None:
        wrongmessage = "User with token is not a valid user"
        return value, wrongmessage

    user.set_first_name(name_first)
    user.set_last_name(name_last)

    value = 1
    return value, wrongmessage


# set user email by token
def usersetemail(data, token, email):
    value = None
    wrongmessage = None

    if token is None:
        wrongmessage = "token doesn't exit"
        return value, wrongmessage

    if check(email) == 0:
        wrongmessage = "Email entered is not a valid email"
        return value, wrongmessage

    if data.check_unique('email', email) == False:
        wrongmessage = "Email address is already being used by another user"
        return value, wrongmessage

    user = data.get_user('token', token)

    if user is None:
        wrongmessage = "User with token is not a valid user"
        return value, wrongmessage

    user.set_email(email)

    value = 1

    return value, wrongmessage


# set user handle by token
def usersethandle(data, token, handle_str):
    value = None
    wrongmessage = None

    if token is None:
        wrongmessage = "token doesn't exit"
        return value, wrongmessage

    if len(handle_str) > 20 or len(handle_str) < 3:
        wrongmessage = "handle_str must be between 3 and 20"
        return value, wrongmessage

    if data.check_unique('handle_str', handle_str) == False:
        wrongmessage = "handle is already used by another user"
        return value, wrongmessage

    user = data.get_user('token', token)

    if user is None:
        wrongmessage = "User with token is not a valid user"
        return value, wrongmessage

    user.set_handle(handle_str)

    value = 1

    return value, wrongmessage

'''
def useruploadphoto(data, token, img_url, x_start, y_start, x_end, y_end):

    wrongmessage = None

    try:
        status = getHttpStatusCode(img_url)

        if status != 200:
            wrongmessage = "img_url is returns an HTTP status other than 200."
            return wrongmessage
    except Exception as e:
        print(e)
        wrongmessage = "img_url is returns an HTTP status other than 200."
        return wrongmessage
        

    user = data.get_user('token', token)
    handle_str = user.handle_str

    imagesource = '../static/' + handle_str + '.jpg'
    urllib.request.urlretrieve(img_url, imagesource)

    imageObject = Image.open(imagesource)

    if imageObject.format != 'JPEG':
        wrongmessage = "Image uploaded is not a JPG"
        return wrongmessage

    if x_start < 0 or x_start > imageObject.size[0] or x_end < 0 or x_end > imageObject.size[0] \
            or y_start < 0 or y_start > imageObject.size[1] or y_end < 0 or y_end > imageObject.size[1] \
            or x_start < x_end or y_start < y_end:
        wrongmessage = "any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL."
        return wrongmessage

    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(imagesource)

    new_photo = 'http://127.0.0.1:5555/static/' + handle_str + '.jpg'
    user.set_photo(new_photo)
    return wrongmessage
'''