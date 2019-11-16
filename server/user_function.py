#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Yimeng
"""
import re
import requests
from PIL import Image
import urllib.request

def getHttpStatusCode(url):
    try:

        request = requests.get(url)

        httpStatusCode = request.status_code

        return httpStatusCode

    except requests.exceptions.HTTPError as e:

        return e


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

    user_observer = data.get_user('token', token)
    if user_observer is None:
        return {'ValueError': 'token not valid'}
    user = data.get_user('u_id', u_id)

    if user is None:
        return {'ValueError': "User with u_id is not a valid user"}

    return user.get_user_detail()


def get_all_users(data, token):

    if data.get_user('token', token) is None:
        return {'ValueError': 'token not valid'}

    return {
        'users': data.get_all_user_detail()
    }
    

# set username by token
def usersetname(data, token, name_first, name_last):

    if token is None:
        return {'ValueError': 'token not valid'}

    if len(name_first) > 50 or len(name_first) < 0:
        return {'ValueError': "name_first is not between 1 and 50 characters in length"}

    if len(name_last) > 50 or len(name_last) < 0:
        return {'ValueError': 'name_last is not between 1 and 50 characters in length'}

    user = data.get_user('token', token)

    if user is None:
        return {'ValueError': 'User with token is not a valid user'}

    user.set_first_name(name_first)
    user.set_last_name(name_last)

    return {}


# set user email by token
def usersetemail(data, token, email):

    if token is None:
        return {'ValueError': "token not valid"}

    if check(email) == 0:
        return {'ValueError': 'Email entered is not a valid email'}

    if not data.check_unique('email', email):
        return {'ValueError': 'Email address is already being used by another user'}

    user = data.get_user('token', token)

    if user is None:
        return {'ValueError': 'User with token is not a valid user'}

    user.set_email(email)
    return {}


# set user handle by token
def usersethandle(data, token, handle_str):

    if token is None:
        return {'ValueError': "token not valid"}

    if len(handle_str) > 20 or len(handle_str) < 3:
        wrongmessage = "handle_str must be between 3 and 20"
        return {'ValueError': "handle_str must be between 3 and 20"}

    if data.check_unique('handle_str', handle_str) == False:
        return {'ValueError': "handle is already used by another user"}

    user = data.get_user('token', token)

    if user is None:
        return {'ValueError': "User with token is not a valid user"}

    user.set_handle(handle_str)
    return {}


def useruploadphoto(data, token, img_url, x_start, y_start, x_end, y_end):

    try:
        status = getHttpStatusCode(img_url)

        if status != 200:
            return {'ValueError': "img_url is returns an HTTP status other than 200."}
    except Exception as e:
        print(e)
        return {'ValueError': "img_url is returns an HTTP status other than 200."}

    user = data.get_user('token', token)
    handle_str = user.handle_str

    imagesource = '../static/' + handle_str + '.jpg'
    urllib.request.urlretrieve(img_url, imagesource)

    imageObject = Image.open(imagesource)

    if imageObject.format != 'JPEG':
        return {'ValueError': "Image uploaded is not a JPG"}

    if x_start < 0 or x_start > imageObject.size[0] or x_end < 0 or x_end > imageObject.size[0] \
            or y_start < 0 or y_start > imageObject.size[1] or y_end < 0 or y_end > imageObject.size[1] \
            or x_start < x_end or y_start < y_end:
        return {
            'ValueError': "any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL."
        }

    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(imagesource)

    new_photo = 'http://127.0.0.1:5555/static/' + handle_str + '.jpg'
    user.set_photo(new_photo)
    return {}

