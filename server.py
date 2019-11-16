#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Angeline, Eric, Meilin, Yimeng
"""
import sys
import os
import pickle
from json import dumps
from flask import Flask, request, send_from_directory
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask_mail import Mail, Message
from server.Data_class import Data
from server.message_function import (
    send_message,
    message_operation,
    react_unreact,
    pin_unpin,
)
from server.extra_function import (
    message_search,
    permission_change,
    standup_message,
    standup_active,
    standup_begin,
)
from server.user_function import (
    usersetemail,
    usersetname,
    usersethandle,
    getprofile,
    get_all_users,
    useruploadphoto,
)
from server.channel_function import (
    ch_create,
    ch_invite,
    ch_details,
    ch_join_leave,
    ch_add_remove_owner,
    ch_lists_listall,
    fun_message,
)
from server.auth_functions import login, logout, register, reset_request, reset


def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__, static_url_path='/static/')
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)



APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'ourteamie4@gmail.com',
    MAIL_PASSWORD = "73python1128!"
)

data = Data()

if os.path.exists(os.getcwd() + '/save.dat') == True:
    if os.path.getsize(os.getcwd() + '/save.dat') > 0:
        data = pickle.load(open('save.dat', 'rb'))

SECRET = 'IE4'


#FIX BELOW
class ValueError(HTTPException):
    code = 400
    message = 'No message specified'


class AccessError(HTTPException):
    code = 400
    message = "No message specified"
# FIX ABOVE


def catch_error_and_return(returned_value):
    if 'ValueError' in returned_value:
        raise ValueError(description=returned_value['ValueError'])
    elif 'AccessError' in returned_value:
        raise AccessError(description=returned_value['AccessError'])


def save():
    global data
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)


# decorator below
def unmarshall(function):
    def wrapper(httpSrc, req=None):
        if req is None:
            req = []
        args = [httpSrc.get(r) for r in req]
        return function(args)
    return wrapper


@unmarshall
def do_get(item):
    return item
# decorator above


@APP.route("/auth/login", methods=['POST'])
def auth_login():

    global data

    email, password = do_get(request.form, ['email', 'password'])
    
    result = login(data, email, password)
    catch_error_and_return(result)
    save()
    return dumps(result)


@APP.route("/auth/logout", methods=['POST'])  # done?
def auth_logout():
    global data

    token = do_get(request.form, ['token'])
    result = logout(data, token)
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route("/auth/register", methods=['POST'])  # done, not checked
def auth_register():
    global data

    email, password, name_first, name_last = do_get(request.form, ['email', 'password', 'name_first', 'name_last'])

    result = register(data, email, password, name_first, name_last)
    catch_error_and_return(result)
    save()
    return dumps(result)


@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_reset_request():
    global data

    email = do_get(request.form, ['email'])
    
    result = reset_request(data, email)
    catch_error_and_return(result)
    mail = Mail(APP)
    try:
        msg = Message("Password reset",
                      sender="ourteamie4@gmail.com",
                      recipients=[email])
        msg.body = result
        mail.send(msg)
    except Exception as e:
        return {'exception': str(e)}

    save()

    return dumps({})


@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_reset():
    global data
    reset_code, new_password = do_get(request.form, ['reset_code', 'new_password'])

    result = reset(data, reset_code, new_password)
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/channels/create', methods=['POST'])
def channel_create():
    global data

    token, channel_name, is_public = do_get(request.form, ['token', 'name', 'is_public'])
    if is_public == "true":
        is_public = True
    else:
        is_public = False
    result = ch_create(data, token, channel_name, is_public)
    catch_error_and_return(result)

    save()

    return dumps(result)


@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    global data

    token, u_id, channel_id = do_get(request.form, ['token', 'u_id', 'channel_id'])
    result = ch_invite(data, token, int(u_id), int(channel_id))
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/channel/details', methods=['GET'])
def channel_details():
    global data

    token, channel_id = do_get(request.args, ['token', 'channel_id'])
    result = ch_details(data, token, int(channel_id))
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/channel/messages', methods=['GET'])
def channel_message():

    global data
    channel_id, token, start = do_get(request.args, ['channel_id', 'token', 'start'])
    result = fun_message(data, token, int(channel_id), int(start))
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/message/sendlater', methods=['POST'])
def message_send_later():
    global data

    message, token, channel_id, time_sent = do_get(request.form, ['message', 'token', 'channel_id', 'time_sent'])
    result = send_message(data, token, int(channel_id), message, float(time_sent))
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/message/send', methods=['POST'])
def message_send():
    global data

    message, token, channel_id = do_get(request.form, ['message', 'token', 'channel_id'])
    result = send_message(data, token, int(channel_id), message)

    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/message/remove', methods=['DELETE'])
def message_remove():
    global data

    message_id, token = do_get(request.form, ['message_id', 'token'])
    result = message_operation(data, token, int(message_id))
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/message/edit', methods=['POST', 'PUT'])
def message_edit():
    global data

    message_id, message, token = do_get(request.form, ['message_id', 'message', 'token'])
    result = message_operation(data, token, int(message_id), message)
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/message/react', methods=['POST'])
def message_react():
    global data

    message_id, react_id, token = do_get(request.form, ['message_id', 'react_id', 'token'])
    result = react_unreact(data, token, int(message_id), int(react_id), 'react')
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/message/unreact', methods=['POST'])
def message_unreact():
    global data

    message_id, react_id, token = do_get(request.form, ['message_id', 'react_id', 'token'])
    result = react_unreact(data, token, int(message_id), int(react_id), 'unreact')
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/message/pin', methods=['POST'])
def message_pin():
    global data

    message_id, token = do_get(request.form, ['message_id', 'token'])
    result = pin_unpin(data, token, int(message_id), 'pin')
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/message/unpin', methods=['POST'])
def message_unpin():
    global data

    message_id, token = do_get(request.form, ['message_id', 'token'])
    result = pin_unpin(data, token, int(message_id), 'unpin')
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    global data

    channel_id, token = do_get(request.form, ['channel_id', 'token'])
    result = ch_join_leave(data, token, int(channel_id), 'leave')
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/channel/join', methods=['POST'])
def channel_join():
    global data

    channel_id, token = do_get(request.form, ['channel_id', 'token'])
    result = ch_join_leave(data, token, int(channel_id), 'join')
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    global data

    channel_id, token, u_id = do_get(request.form, ['channel_id', 'token', 'u_id'])
    result = ch_add_remove_owner(data, token, int(channel_id), int(u_id), 'add')
    catch_error_and_return(result)

    save()
    return dumps(result)


@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    global data

    channel_id, token, u_id = do_get(request.form, ['channel_id', 'token', 'u_id'])
    result = ch_add_remove_owner(data, token, int(channel_id), int(u_id), 'remove')
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/channels/list', methods=['GET'])
def channel_list():
    global data

    token = do_get(request.args, ['token'])[0]
    result = ch_lists_listall(data, token, 'lists')
    catch_error_and_return(result)
    return dumps(result)


@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    global data

    token = do_get(request.args, ['token'])[0]
    result = ch_lists_listall(data, token, 'listall')
    catch_error_and_return(result)
    return dumps(result)


@APP.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('', path)


@APP.route('/user/profile', methods=['GET'])
def profile():
    global data

    token, u_id = do_get(request.args, ['token', 'u_id'])
    result = getprofile(data, token, int(u_id))

    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/users/all', methods=['GET'])
def users_all():
    global data

    token = do_get(request.args, ['token'])[0]
    result = get_all_users(data, token)
    catch_error_and_return(result)
    save()

    return dumps(result)
    

@APP.route('/user/profile/setname', methods=['PUT'])
def setname():
    global data

    token, name_first, name_last = do_get(request.form, ['token', 'name_first', 'name_last'])
    result = usersetname(data, token, name_first, name_last)

    catch_error_and_return(result)
    save()
    return dumps(result)


@APP.route('/user/profile/setemail', methods=['PUT'])
def setemail():
    global data

    token, email = do_get(request.form, ['token', 'email'])
    result = usersetemail(data, token, email)

    catch_error_and_return(result)
    save()
    return dumps(result)


@APP.route('/user/profile/sethandle', methods=['PUT'])
def sethandle():
    global data

    token, handle_str = do_get(request.form, ['token', 'handle_str'])
    result = usersethandle(data, token, handle_str)

    catch_error_and_return(result)
    save()
    return dumps(result)


@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def uploadphoto():

    global data

    token, img_url, x_start, y_start, x_end, y_end  = do_get(request.form, ['token', 'img_url', 'x_start', 'y_start', 'x_end', 'y_end'])
    print(token, img_url, x_start, x_end, y_start, y_end)
    result = useruploadphoto(data,token, img_url, x_start, x_end, y_start, y_end)

    catch_error_and_return(result)
    save()
    return dumps(result)


@APP.route('/search', methods=['GET'])
def search():
    global data

    token, query_str = do_get(request.args, ['token', 'query_str'])
    result = message_search(data, token, query_str)
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/admin/userpermission/change', methods=['POST'])
def change_permission():

    global data

    token, u_id, permission_id = do_get(request.form, ['token', 'u_id', 'permission_id'])
    result = permission_change(data, token, u_id, int(permission_id))
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/standup/start', methods=['POST'])
def standup_start():
    global data

    token, channel_id, length = do_get(request.form, ['token', 'channel_id', 'length'])
    result = standup_begin(data, token, int(channel_id), int(length))

    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/standup/active', methods=['GET'])
def standup_activate():
    global data

    token, channel_id = do_get(request.args, ['token', 'channel_id'])
    result = standup_active(data, token, int(channel_id))
    catch_error_and_return(result)
    save()

    return dumps(result)


@APP.route('/standup/send', methods=['POST'])
def standup_send():
    global  data

    token, channel_id, message = do_get(request.form, ['token', 'channel_id', 'message'])
    result = standup_message(data, token, int(channel_id), message)

    catch_error_and_return(result)
    save()

    return dumps(result)


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
