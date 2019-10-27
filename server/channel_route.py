from flask import Flask, request
from json import dumps
from werkzeug.exceptions import HTTPException
from channel_function import (
        ch_create,
        ch_invite,
        ch_details,
        ch_leave,
        ch_join,
        ch_addowner,
        ch_removeowner,
        ch_lists,
        ch_listall
)
APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True


data = {
    'users': [
            {'u_id': 123,
             'name_first': 'test',
             'name_last': 'test',
             'token': '12345',
             'handle_str': 'testtest',
             'email': 'test@test.com',
             'password': 'test',
             'permission_id': 1,
             'channel_involve': [0]  # channel_id
             },
            {'u_id': 1234,
             'name_first': 'test2',
             'name_last': 'test2',
             'token': '123456',
             'handle_str': 'testtest2',
             'email': 'test2@test2.com',
             'password': 'test2',
             'permission_id': 3,
             'channel_involve': [0]  # channel_id
             }
        ],
    'channels': [{
        'name': 'test',
        'channel_id': 0,
        'user_list': [
            {'u_id': 123, 'name_first': 'test', 'name_last': 'test',\
             'is_owner': True},
            {'u_id': 1234, 'name_first': 'test2', 'name_last': 'test2',\
             'is_owner': False}
        ],
        'is_public': True
    }],
    'messages': [
            {
                'message': 'test',
                'u_id': 123,
                'reacts': [{'react_id': 1, 'u_ids': []}],
                'is_pinned': False,
                'time_created': '10/20/2019, 23:25:33',
                'channel_id': 1,
                'message_id': 0
            }
    ],
    'counter': {
        'user': 1,
        'channel': 1,
        'message': 1
    }
}


class ValueError(HTTPException):
    code = 400
    message = 'No message specified'


class Exception(HTTPException):
    code = 400
    message = "No message specified"


@APP.route('/channels/create', methods=['POST'])
def channels_create():
    global data
    token = request.form.get('token')
    channel_name = request.form.get('channel_name')
    is_public = request.form.get('is_public')
    if is_public == "true":
        is_public = True
    else:
        is_public = False
    channel_id = ch_create(data, token, channel_name, is_public)
    if 'ValueError' in channel_id:
        raise ValueError(description=channel_id['ValueError'])
    return dumps(channel_id)


@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    global data
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    channel_id = request.form.get('channel_id')
    result = ch_invite(data, token, u_id, channel_id)
    if 'ValueError' in result:
        raise ValueError(description=result['ValueError'])
    elif 'AccessError' in result:
        raise AccessError(description=result['AccessError'])
    return dumps()


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
    return dumps(channel_detail)


@APP.route('/channel/message', methods=['GET'])
def channel_message():

    return dumps({})


@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    global data
    channel_id = int(request.form.get('channel_id'))
    token = request.form.get('token')
    output = ch_leave(data, token, channel_id)
    if 'ValueError' in output:
        raise ValueError(description=output['ValueError'])
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
    return dumps(removeowner)


@APP.route('/channels/list', methods=['GET'])
def channel_list():
    global data
    print(data)
    token = request.args.get('token')
    return dumps(ch_lists(data, token))


@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    global data
    token = request.args.get('token')
    listall = ch_listall(data, token)
    return dumps(listall)


if __name__ == '__main__':
    APP.run(port=11280, debug=True)
