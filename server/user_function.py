#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Yimeng
"""
import re
import string
import requests
from PIL import Image
import urllib.request
from flask import request
from server.helper import check_valid_email, authorise


def getHttpStatusCode(url):
    try:

        request = requests.get(url)

        httpStatusCode = request.status_code

        return httpStatusCode

    except requests.exceptions.HTTPError as e:

        return e


# get user profile by token
@authorise
def getprofile(data, user, u_id, host):

    user_target = data.get_element('users_group', 'u_id', u_id)

    if user_target is None:
        return {'ValueError': "User with u_id is not a valid user"}

    return user_target.get_user_detail('individual', host)


@authorise
def get_all_users(data, user, host):

    return {
        'users': data.get_all_user_detail(host)
    }


# set username by token
@authorise
def usersetname(data, user, name_first, name_last):

    if len(name_first) > 50 or len(name_first) < 0:
        return {'ValueError': "name_first is not between 1 and 50 characters \
in length"}

    if len(name_last) > 50 or len(name_last) < 0:
        return {'ValueError': 'name_last is not between 1 and 50 characters in\
 length'}

    if user is None:
        return {'ValueError': 'User with token is not a valid user'}

    user.set_first_name(name_first)
    user.set_last_name(name_last)

    return {}


# set user email by token
@authorise
def usersetemail(data, user, email):

    if check_valid_email(email) != {}:
        return {'ValueError': 'Email entered is not a valid email'}

    if not data.check_unique('users_group', 'email', email):
        return {'ValueError': 'Email address is already being used by another \
user'}

    user.set_email(email)
    return {}


# set user handle by token
@authorise
def usersethandle(data, user, handle_str):

    if len(handle_str) > 20 or len(handle_str) < 3:
        return {'ValueError': "handle_str must be between 3 and 20"}

    if not data.check_unique('users_group', 'handle_str', handle_str):
        return {'ValueError': "handle is already used by another user"}

    user.set_handle(handle_str)
    return {}


@authorise
def useruploadphoto(data, user, img_url, x_start, y_start, x_end, y_end):

    try:
        status = getHttpStatusCode(img_url)

        if status != 200:
            return {'ValueError': "img_url is returns an HTTP status other \
than 200."}
    except Exception as e:
        print(e)
        return {'ValueError': "img_url is returns an HTTP status other than \
200."}

    u_id = str(user.u_id)

    imagesource = './static/' + u_id + '.jpg'
    urllib.request.urlretrieve(img_url, imagesource)

    imageObject = Image.open(imagesource)

    if imageObject.format != 'JPEG':
        return {'ValueError': "Image uploaded is not a JPG"}

    x_start = int(x_start)
    y_start = int(y_start)
    x_end = int(x_end)
    y_end = int(y_end)

    if x_start < 0 or x_start > imageObject.size[0] \
            or x_end < 0 or x_end > imageObject.size[0] \
            or y_start < 0 or y_start > imageObject.size[1] \
            or y_end < 0 or y_end > imageObject.size[1] \
            or x_start > x_end or y_start > y_end:
        return {
            'ValueError': "any of x_start, y_start, x_end, y_end are not \
 within the dimensions of the image at the URL."
        }

    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(imagesource)

    new_photo = request.host_url + 'static/' + u_id + '.jpg'
    user.set_photo(new_photo)
    return {}
