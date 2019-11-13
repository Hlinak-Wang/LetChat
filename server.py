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
from datetime import datetime, timezone
from flask_mail import Mail, Message
from server.Data_class import Data
from server.message_function import fun_send, fun_remove, fun_edit, react_unreact, \
    pin_unpin
#from server.extra_function import message_search, permission_change, fun_standup_send, fun_standup_star
from server.user_function import usersetemail, usersetname, usersethandle, getprofile
from server.channel_function import (
    ch_create,
    ch_invite,
    ch_details,
    ch_leave,
    ch_join,
    ch_addowner,
    ch_removeowner,
    ch_lists,
    ch_listall,
    fun_message,
)
from server.auth_functions import login, logout, register, reset_request, reset

"""
import functions from another file
"""
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


def save():
    global data
    with open('save.dat', 'wb') as FILE:
        pickle.dump(data, FILE, True)

"""
def send_message_buffer():
    global data
    time_now = datetime.now()
    for message in data['message_buffer'][:]:
        time_send = datetime.strptime(message['time_created'],  "%H:%M")
        channel = find_channel(data, message['channel_id'])
        if time_send < time_now:
            channel['messages'].append(message)
            data['message_buffer'].remove(message)


def pop_queue():
    global data
    time_now = datetime.now()
    time_now = time_now.replace(tzinfo=timezone.utc).timestamp()
    for channel in data['channels']:
        if 'standup' in channel:
            standup = channel['standup']
            if standup['time_finish'] == '1/1/1900, 1:00:00' or time_now > standup['time_finish']:
                if channel['standup_message'] != "":

                    channel['messages'].insert(0, {
                        'u_id': standup['u_id'],
                        'message_id': data['message_counter'],
                        'message': channel['standup_message'],
                        'time_created': time_now,
                        'reacts': [{'react_id': 1, 'u_ids': []}],
                        'is_pinned': False,
                    })
                    channel['standup_message'] = ""
                    data['message_counter'] += 1
"""

@APP.route("/auth/login", methods=['POST'])
def auth_login():

    global data

    email = request.form.get('email')
    password = request.form.get('password')
    result = login(data, email, password)
    save()
    return dumps(result)


@APP.route("/auth/logout", methods=['POST'])  # done?
def auth_logout():
    global data

    token = request.form.get('token')
    result = logout(data, token)
    save()

    return dumps(result)


@APP.route("/auth/register", methods=['POST'])  # done, not checked
def auth_register():
    global data

    email = request.form.get('email')

    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

    result = register(data, email, password, name_first, name_last)
    save()
    return dumps(result)


@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_reset_request():
    global data

    email = request.form.get('email')
    code = reset_request(data, email)

    mail = Mail(APP)

    try:
        msg = Message("Password reset",
                      sender="ourteamie4@gmail.com",
                      recipients=[email])
        msg.body = code
        mail.send(msg)
    except Exception as e:
        return {'exception': str(e)}

    save()

    return dumps({})


@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_reset():
    global data
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')

    result = reset(data, reset_code, new_password)
    save()

    return dumps(result)


@APP.route('/channels/create', methods=['POST'])
def channel_create():
    global data

    token = request.form.get('token')
    channel_name = request.form.get('name')
    is_public = request.form.get('is_public')
    if is_public == "true":
        is_public = True
    else:
        is_public = False
    channel_id = ch_create(data, token, channel_name, is_public)
    if 'ValueError' in channel_id:
        raise ValueError(description=channel_id['ValueError'])

    save()

    return dumps(channel_id)


@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    global data

    token = request.form.get('token')
    u_id = int(request.form.get('u_id'))
    channel_id = int(request.form.get('channel_id'))
    result = ch_invite(data, token, u_id, channel_id)
    if 'ValueError' in result:
        raise ValueError(description=result['ValueError'])
    elif 'AccessError' in result:
        raise AccessError(description=result['AccessError'])
    save()

    return dumps(result)


@APP.route('/channel/details', methods=['GET'])
def channel_details():
    global data

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    channel_detail = ch_details(data, token, channel_id)
    if 'ValueError' in channel_detail:
        raise ValueError(description=channel_detail['ValueError'])
    elif 'AccessError' in channel_detail:
        raise AccessError(description=channel_detail['AccessError'])
    save()

    return dumps(channel_detail)


@APP.route('/channel/messages', methods=['GET'])
def channel_message():

    channel_id = int(request.args.get('channel_id'))
    token = request.args.get('token')
    start = int(request.args.get('start'))
    messages = fun_message(data, token, channel_id, start)
    if 'ValueError' in messages:
        raise ValueError(description=messages['ValueError'])
    elif 'AccessError' in messages:
        raise AccessError(description=messages['AccessError'])
    save()

    return dumps(messages)


@APP.route('/message/send_later', methods=['POST'])
def message_send_later():
    global data
    message = request.form.get('message')
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    time_create = request.form.get('time_create')

    output = fun_send(data, token, channel_id, message, time_create)
    save()

    return dumps(output)


@APP.route('/message/send', methods=['POST'])
def message_send():
    global data
    message = request.form.get('message')
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    output = fun_send(data, token, channel_id, message)

    # save()
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    save()

    return dumps(output)


@APP.route('/message/remove', methods=['DELETE'])
def message_remove():
    global data
    message_id = int(request.form.get('message_id'))
    token = request.form.get('token')
    output = fun_remove(data, token, message_id)
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    save()

    return dumps(output)


@APP.route('/message/edit', methods=['POST', 'PUT'])
def message_edit():
    global data
    message_id = int(request.form.get('message_id'))
    message = request.form.get('message')
    token = request.form.get('token')
    output = fun_edit(data, token, message_id, message)
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    save()

    return dumps(output)


@APP.route('/message/react', methods=['POST'])
def message_react():
    global data
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    token = request.form.get('token')

    output = react_unreact(data, token, message_id, react_id, 'react')
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    save()

    return dumps(output)


@APP.route('/message/unreact', methods=['POST'])
def message_unreact():
    global data
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    token = request.form.get('token')
    output = react_unreact(data, token, message_id, react_id, 'unreact')
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    save()

    return dumps(output)


@APP.route('/message/pin', methods=['POST'])
def message_pin():
    global data

    message_id = int(request.form.get('message_id'))
    token = request.form.get('token')
    output = pin_unpin(data, token, message_id, 'pin')
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    save()

    return dumps(output)


@APP.route('/message/unpin', methods=['POST'])
def message_unpin():
    global data

    message_id = int(request.form.get('message_id'))
    token = request.form.get('token')
    output = pin_unpin(data, token, message_id, 'unpin')
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    save()

    return dumps(output)


@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    global data

    channel_id = int(request.form.get('channel_id'))
    token = request.form.get('token')
    output = ch_leave(data, token, channel_id)
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    save()

    return dumps(output)


@APP.route('/channel/join', methods=['POST'])
def channel_join():
    global data

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    join = ch_join(data, token, channel_id)
    if 'ValueError' in join:
        raise ValueError(description=join['ValueError'])
    elif 'AccessError' in join:
        raise AccessError(description=join['AccessError'])
    save()

    return dumps(join)


@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    global data

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    addowner = ch_addowner(data, token, channel_id, u_id)
    if 'ValueError' in addowner:
        raise ValueError(description=addowner['ValueError'])
    elif 'AccessError' in addowner:
        raise AccessError(description=addowner['AccessError'])

    save()
    return dumps(addowner)


@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    global data

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    removeowner = ch_removeowner(data, token, channel_id, u_id)
    if 'ValueError' in removeowner:
        raise ValueError(description=removeowner['ValueError'])
    elif 'AccessError' in removeowner:
        raise AccessError(description=removeowner['AccessError'])
    save()

    return dumps(removeowner)


@APP.route('/channels/list', methods=['GET'])
def channel_list():
    global data

    token = request.args.get('token')
    print(token)
    return dumps(ch_lists(data, token))


@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    global data

    token = request.args.get('token')
    listall = ch_listall(data, token)
    return dumps(listall)


@APP.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('', path)


@APP.route('/user/profile', methods=['GET'])
def profile():
    global data

    token = request.args.get('token')
    u_id = request.args.get('u_id')

    (value, Errormessage) = getprofile(data, token, u_id)

    if value == None:
        raise ValueError(description=Errormessage)
    save()

    return dumps(value)


@APP.route('/user/profile/setname', methods=['PUT'])
def setname():
    global data

    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

    (value, Errormessage) = usersetname(data, token, name_first, name_last)

    if value == None:
        raise ValueError(description=Errormessage)
    save()
    return dumps({})


@APP.route('/user/profile/setemail', methods=['PUT'])
def setemail():
    global data

    token = request.form.get('token')
    email = request.form.get('email')

    (value, Errormessage) = usersetemail(data, token, email)

    if value == None:
        raise ValueError(description=Errormessage)
    save()

    return dumps({})


@APP.route('/user/profile/sethandle', methods=['PUT'])
def sethandle():
    global data

    token = request.form.get('token')
    handle_str = request.form.get('handle_str')

    (value, Errormessage) = usersethandle(data, token, handle_str)

    if value == None:
        raise ValueError(description=Errormessage)
    save()

    return dumps({})


@APP.route('/user/profile/uploadphoto', methods=['POST'])
def uploadphoto():
    # (note: this is not requried to be completed until iteration 3)

    return dumps({})

"""
@APP.route('/search', methods=['GET'])
def search():
    global data
    pop_queue()
    send_message_buffer()
    query_str = request.args.get('query_str')
    token = request.args.get('token')
    output = message_search(data, token, query_str)
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    save()

    return dumps(output)


@APP.route('/admin/userpermission/change', methods=['POST'])
def change_permission():

    global data

    token = request.form.get('token')
    u_id = request.form.get('u_id')
    permission_id = int(request.form.get('permission_id'))
    output = permission_change(data, token, u_id, permission_id)
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    save()

    return dumps(output)


@APP.route('/standup/start', methods=['POST'])
def standup_start():
    global data

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))

    output = fun_standup_star(data, token, channel_id)

    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    save()

    return dumps(output)


@APP.route('/standup/send', methods=['POST'])
def standup_send():

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')

    output = fun_standup_send(data, token, channel_id, message)

    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
    if 'AccessError' in output:
        raise AccessError(description=output['AccessError'])
    save()

    return dumps(output)
"""

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
