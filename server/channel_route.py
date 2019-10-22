from flask import Flask, request
from json import dumps
from channel_function import ch_create, ch_invite,ch_details, ch_leave, ch_join, ch_addowner, ch_removeowner, ch_lists, ch_listall
APP = Flask(__name__)


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
             'channel_involve': [1]  # channel_id
             },
            {'u_id': 1234,
             'name_first': 'test2',
             'name_last': 'test2',
             'token': '123456',
             'handle_str': 'testtest2',
             'email': 'test2@test2.com',
             'password': 'test2',
             'permission_id': 3,
             'channel_involve': [1]  # channel_id
             }
        ],
        'channels': [{
            'name': 'test',
            'channel_id': 1,
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


@APP.route('/channels/create', methods=['POST'])
def channel_create():
    global data
    token = request.form.get('token')
    channel_name = int(request.form.get('channel_name'))
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
    return dumps(ch_leave())


@APP.route('/channel/join', methods=['POST'])
def channel_join():
    return dumps(ch_join())


@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    return dumps(ch_addowner())


@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    return dumps(ch_removeowner())


@APP.route('/channels/list', methods=['GET'])
def channel_list():
    lists = ch_lists
    return dumps(lists)


@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    listall = ch_listall()
    return dumps(listall)


if __name__ == '__main__':
    APP.run(port=11280,debug = True)
