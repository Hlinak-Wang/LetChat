"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request
from channel_function import ch_create, ch_invite, ch_details,\
ch_leave, ch_join, ch_addowner, ch_removeowner, ch_lists, ch_listall
APP = Flask(__name__)
CORS(APP)

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
            {'u_id': 123, 'name_first': 'test', 'name_last': 'test', 'is_owner': True},
            {'u_id': 1234, 'name_first': 'test2', 'name_last': 'test2', 'is_owner': False}
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

@APP.route('/auth/register', methods=['POST'])
def echo4():
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    email = request.form.get('email')
    password = request.form.get('password')

    return dumps({'u_id': 12354, 'token': '123'}) 

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

@APP.route('/channels/create', methods=['POST'])
def channel_create():
    global data
    token = request.form.get('token')
    channel_name = request.form.get('channel_name')
    is_public = request.form.get('is_public')
    channel_id = ch_create(data, token, channel_name, is_public)
    return dumps(channel_id)


@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    global data
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    channel_id = request.form.get('channel_id')
    return dumps(ch_invite(data, token, u_id, channel_id))


@APP.route('/channel/details', methods=['GET'])
def channel_details():
    global data
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    channel_detail = ch_details(data, token, channel_id)
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
    #if 'ValueError' in output:
     #   return 400
    return dumps(output)


@APP.route('/channel/join', methods=['POST'])
def channel_join():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return dumps(ch_join(data, token, channel_id))


@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(ch_addowner(data, token, channel_id, u_id))


@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    global data
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(ch_removeowner(data, token, channel_id, u_id))


@APP.route('/channels/list', methods=['GET'])
def channel_list():
    global data
    token = request.args.get('token')
    return dumps(ch_lists(data, token))


@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    global data
    token = request.args.get('token')
    listall = ch_listall(data, token)
    return dumps(listall)

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
