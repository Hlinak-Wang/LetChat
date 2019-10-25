import datetime
from server.message_function import fun_send_late, fun_send, fun_remove, fun_edit, fun_react, fun_unreact, fun_pin, \
    fun_unpin


# initial state of testing
def getdata():
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
             },
            {'u_id': 12345,
             'name_first': 'not in channel',
             'name_last': 'test',
             'token': '1234567',
             'handle_str': 'not in channel',
             'email': 'tests2@tests2.com',
             'password': 'tesst2',
             'permission_id': 3,
             'channel_involve': []  # channel_id
             }
        ],
        'channels': [{
            'name': 'test',
            'channel_id': 1,
            'user_list': [
                {'u_id': 123, 'name_first': 'test', 'name_last': 'test', 'is_owner': True},
                {'u_id': 1234, 'name_first': 'test2', 'name_last': 'test2', 'is_owner': False}
            ],
            'is_public': True,
            'standup': {'time_finish': '1/1/1900, 1:00:00', 'u_id': None},    # time_finish
            'messages': [
                {
                    'message': 'test',
                    'u_id': 123,
                    'reacts': [{'react_id': 1, 'u_ids': []}],
                    'is_pinned': False,
                    'time_created': '10/20/2019, 23:25:33',
                    'message_id': 1,
                    'channel_id': 1
                },
                {
                    'message': 'test2',
                    'u_id': 1234,
                    'reacts': [{'react_id': 1, 'u_ids': []}],
                    'is_pinned': False,
                    'time_created': '10/20/2019, 23:24:33',
                    'message_id': 0,
                    'channel_id': 1
                }
            ]
        }],
        'message_counter': 0,
        'message_buffer': []
    }
    return data


def test_send_late():
    data = getdata()
    user = data['users'][0]
    channel = data['channels'][0]
    message_long = ""
    for i in range(0, 1010):
        message_long += "a"
    time_valid = '23:59'
    time_invalid = '00:00'
    # Invalid input
    assert fun_send_late(data, 'asdf', channel["channel_id"], 'short', time_valid) == {'AccessError': 'User not exist'}

    assert fun_send_late(data, user["token"], channel["channel_id"], message_long, time_valid) == {
           "ValueError": "Message is more than 1000 characters"
    }
    assert fun_send_late(data, user["token"], 1232, 'short_message', time_valid) == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'
    }

    assert fun_send_late(data, user["token"], channel["channel_id"], 'short_message', time_invalid) == {
        'ValueError': 'Time sent is a time in the past'
    }

    # Valid input
    output = fun_send_late(data, user["token"], channel["channel_id"], 'short_message', time_valid)
    assert output == {'message_id': 0}

def test_send():
    data = getdata()
    user = data['users'][0]
    channel = data['channels'][0]
    message_long = ""
    for i in range(0, 1010):
        message_long += "a"

    # Invalid input
    assert fun_send(data, user["token"], channel["channel_id"], message_long) == {
        "ValueError": "Message is more than 1000 characters"}
    assert fun_send(data, user["token"], 2, 'short_message') == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'}

    # Valid input
    output = fun_send(data, user["token"], channel["channel_id"], 'short_message')
    assert output == {'message_id': 0}
    assert channel['messages'][0]['message'] == 'short_message'


def test_remove():
    data = getdata()
    user_admin = data['users'][0]
    user_norm = data['users'][1]
    channel = data['channels'][0]

    # Invalid input
    assert fun_remove(data, user_norm["token"], 1) == {'AccessError': 'permission denied'}
    assert fun_remove(data, user_norm["token"], 100) == {'ValueError': 'Message (based on ID) no longer exists'}

    output = fun_remove(data, user_admin['token'], 0)
    assert output == {}
    assert channel['messages'] == [
        {
            'message': 'test',
            'u_id': 123,
            'reacts': [{'react_id': 1, 'u_ids': []}],
            'is_pinned': False,
            'time_created': '10/20/2019, 23:25:33',
            'message_id': 1,
            'channel_id': 1
        }
    ]


def test_edit():
    data = getdata()
    user_admin = data['users'][0]
    user_norm = data['users'][1]
    channel = data['channels'][0]

    # Invalid input
    assert fun_edit(data, user_norm["token"], 1, "new_message") == {'AccessError': 'permission denied'}
    assert fun_edit(data, user_norm["token"], 100, "new_message") == {
        'ValueError': 'Message (based on ID) no longer exists'}

    # Valid input
    output = fun_edit(data, user_admin["token"], 0, "new_message")
    assert output == {}
    assert channel['messages'] == [{
        'message': 'test',
        'u_id': 123,
        'reacts': [{'react_id': 1, 'u_ids': []}],
        'is_pinned': False,
        'time_created': '10/20/2019, 23:25:33',
        'message_id': 1,
        'channel_id': 1
    },
        {
            'message': 'new_message',
            'u_id': 1234,
            'reacts': [{'react_id': 1, 'u_ids': []}],
            'is_pinned': False,
            'time_created': '10/20/2019, 23:24:33',
            'message_id': 0,
            'channel_id': 1
        }]


def test_react():
    data = getdata()
    user = data['users'][0]
    channel = data['channels'][0]

    # Invalid input
    assert fun_react(data, user["token"], 100, 1) == {'ValueError': 'Message (based on ID) no longer exists'}

    assert fun_react(data, user["token"], 1, 100) == {'ValueError': 'react_id is not a valid React ID'}

    # React the message in advance
    # If the next text raises an exception means the react is successfully added
    output = fun_react(data, user["token"], 1, 1)
    assert output == {}
    assert channel['messages'][0] == {
        'message': 'test',
        'u_id': 123,
        'reacts': [{'react_id': 1, 'u_ids': [123]}],
        'is_pinned': False,
        'time_created': '10/20/2019, 23:25:33',
        'message_id': 1,
        'channel_id': 1
    }

    # React the message again see whether raise exception
    assert fun_react(data, user["token"], 1, 1) == {'ValueError': 'user has reacted'}


def test_unreact():
    data = getdata()
    user = data['users'][0]
    channel = data['channels'][0]

    # Invalid input
    assert fun_unreact(data, user["token"], 100, 1) == {'ValueError': 'Message (based on ID) no longer exists'}

    assert fun_unreact(data, user["token"], 1, 100) == {'ValueError': 'react_id is not a valid React ID'}

    # React the message for testing in advance
    output = fun_react(data, user["token"], 1, 1)

    # Unreact the message again see whether raise excepion
    output = fun_unreact(data, user["token"], 1, 1)
    assert output == {}
    assert channel['messages'][0] == {
        'message': 'test',
        'u_id': 123,
        'reacts': [{'react_id': 1, 'u_ids': []}],
        'is_pinned': False,
        'time_created': '10/20/2019, 23:25:33',
        'message_id': 1,
        'channel_id': 1
    }
    # React the message again see whether raise exception
    assert fun_unreact(data, user["token"], 1, 1) == {'ValueError': 'user has not reacted'}


def test_pin():
    data = getdata()
    user_admin = data['users'][0]
    user_norm = data['users'][1]
    user_not_in_channel = data['users'][2]
    channel = data['channels'][0]

    # Invalid input
    assert fun_pin(data, user_admin['token'], 100) == {'ValueError': 'message_id is not a valid message'}

    assert fun_pin(data, user_norm['token'], 1) == {'ValueError': 'The authorised user is not an admin'}

    assert fun_pin(data, user_not_in_channel['token'], 1) == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    # Pin the message in advance, if the next test raise exception
    # means the message is successfully pinned
    output = fun_pin(data, user_admin['token'], 1)
    assert output == {}
    assert channel['messages'][0] == {
        'message': 'test',
        'u_id': 123,
        'reacts': [{'react_id': 1, 'u_ids': []}],
        'is_pinned': True,
        'time_created': '10/20/2019, 23:25:33',
        'message_id': 1,
        'channel_id': 1
    }

    assert fun_pin(data, user_admin['token'], 1) == {"ValueError": "Message with ID message_id is already pinned"}


def test_unpin():
    data = getdata()
    user_admin = data['users'][0]
    user_norm = data['users'][1]
    user_not_in_channel = data['users'][2]
    channel = data['channels'][0]

    # Invalid input
    assert fun_unpin(data, user_admin['token'], 100) == {'ValueError': 'message_id is not a valid message'}

    assert fun_unpin(data, user_norm['token'], 1) == {'ValueError': 'The authorised user is not an admin'}

    assert fun_unpin(data, user_not_in_channel['token'], 1) == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    assert fun_unpin(data, user_admin['token'], 1) == {"ValueError": "Message with ID message_id is already unpinned"}

    # Pin the message in advance, if the next test raise exception
    # means the message is successfully pinned
    output = fun_pin(data, user_admin['token'], 1)
    output = fun_unpin(data, user_admin['token'], 1)
    assert output == {}
    assert channel['messages'][0] == {
        'message': 'test',
        'u_id': 123,
        'reacts': [{'react_id': 1, 'u_ids': []}],
        'is_pinned': False,
        'time_created': '10/20/2019, 23:25:33',
        'message_id': 1,
        'channel_id': 1
    }
