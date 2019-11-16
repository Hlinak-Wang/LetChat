#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from server.message_function import fun_send, message_operation, react_unreact, pin_unpin
from datetime import datetime
from server.Data_class import Data
from server.auth_functions import register
from server.channel_function import ch_create, ch_join_leave


# initial state of testing
def generate_data():
    test_data = Data()
    user_admin = register(test_data, 'test1@test.com', 'password', 'name_first1', 'name_last')
    user_channel_owner = register(test_data, 'test2@test.com', 'password', 'name_first2', 'name_last')
    user_in_channel = register(test_data, 'test4@test.com', 'password', 'name_first4', 'name_last')
    user_notin_channel = register(test_data, 'test3@test.com', 'password', 'name_first3', 'name_last')

    channel = ch_create(test_data, user_channel_owner['token'], 'test_channel', True)
    ch_join_leave(test_data, user_admin['token'], channel['channel_id'], 'join')
    ch_join_leave(test_data, user_in_channel['token'], channel['channel_id'], 'join')

    fun_send(test_data, user_in_channel['token'], channel['channel_id'], 'test3')
    fun_send(test_data, user_channel_owner['token'], channel['channel_id'], 'test2')
    fun_send(test_data, user_admin['token'], channel['channel_id'], 'test')

    return test_data


def getting_user(data):
    user_admin = data.users_group[0]
    user_channel_owner = data.users_group[1]
    user_in_channel = data.users_group[2]
    user_not_inchannel = data.users_group[3]

    return user_admin, user_channel_owner, user_in_channel, user_not_inchannel


def getting_message(data):
    message_admin = data.messages_group[0]
    message_owner = data.messages_group[1]
    message_norm = data.messages_group[2]

    return message_admin, message_norm, message_owner


def getting_channel(data):
    channel = data.channels_group[0]
    return channel


def test_send_late_bad():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    channel = getting_channel(data)

    message_long = ""
    for i in range(0, 1010):
        message_long += "a"

    time_valid = datetime.now().timestamp() + 10
    time_invalid = datetime.now().timestamp() - 10
    # Invalid input
    assert fun_send(data, user_admin.token, channel.channel_id, message_long, time_valid) == {
           "ValueError": "Message is more than 1000 characters"
    }
    assert fun_send(data, user_notin_channel.token, 1232, 'short_message', time_valid) == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'
    }

    assert fun_send(data, user_admin.token, channel.channel_id, 'short_message', time_invalid) == {
        'ValueError': 'Time sent is a time in the past'
    }


def test_send_late_good():
    data = generate_data()
    user_admin = getting_user(data)[0]
    channel = getting_channel(data)

    time_valid = datetime.now().timestamp() + 10

    output = fun_send(data, user_admin.token, channel.channel_id, 'short_message', time_valid)
    assert data.get_message(output['message_id']) is not None


def test_send_bad():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    channel = getting_channel(data)

    message_long = ""
    for i in range(0, 1010):
        message_long += "a"

    assert fun_send(data, user_admin.token, channel.channel_id, message_long) == {
        "ValueError": "Message is more than 1000 characters"}

    assert fun_send(data, user_notin_channel.token, 2, 'short_message') == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'}


def test_send_good():
    data = generate_data()
    user_admin = getting_user(data)[0]
    channel = getting_channel(data)

    output = fun_send(data, user_admin.token, channel.channel_id, 'short_message')
    assert data.get_message(output['message_id']) is not None


def test_remove_bad():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin, message_owner, message_norm = getting_message(data)

    assert message_operation(data, user_in_channel.token, message_admin.message_id) == {'AccessError': 'permission denied'}
    assert message_operation(data, user_in_channel.token, 100) == {'ValueError': 'Message (based on ID) no longer exists'}


def test_remove_good():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin, message_owner, message_norm = getting_message(data)
    channel = getting_channel(data)

    # case 1
    output = message_operation(data, user_admin.token, message_admin.message_id)
    assert output == {}
    assert data.get_message(message_admin.message_id) is None

    # case 2
    output = message_operation(data, user_owner.token, message_norm.message_id)
    assert output == {}
    assert data.get_message(message_norm.message_id) is None

    # case 3
    new_message = fun_send(data, user_in_channel.token, channel.channel_id, "new")
    output = message_operation(data, user_in_channel.token, new_message["message_id"])
    assert output == {}
    assert data.get_message(new_message['message_id']) is None


def test_edit_bad():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin, message_owner, message_norm = getting_message(data)

    assert message_operation(data, user_in_channel.token, message_admin.message_id, "new_message") == {
        'AccessError': 'permission denied'
    }

    assert message_operation(data, user_admin.token, 100, "new_message") == {
        'ValueError': 'Message (based on ID) no longer exists'
    }


def test_edit_good():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin, message_owner, message_norm = getting_message(data)
    channel = getting_channel(data)

    # case 1
    output = message_operation(data, user_admin.token, message_admin.message_id, "new_message")
    assert output == {}
    assert message_admin.message == "new_message"

    # case 2
    output = message_operation(data, user_owner.token, message_norm.message_id, "owner_change")
    assert output == {}
    assert message_norm.message == "owner_change"

    # case 3
    new_message = fun_send(data, user_in_channel.token, channel.channel_id, "new")
    output = message_operation(data, user_in_channel.token, new_message["message_id"], "norm user change")
    assert output == {}
    assert data.get_message(new_message['message_id']).message == "norm user change"


def test_react_bad():
    data = generate_data()
    user_admin = getting_user(data)[0]
    message_admin= getting_message(data)[0]

    assert react_unreact(data, user_admin.token, 100, 1, 'react') == {'ValueError': 'Message (based on ID) no longer exists'}

    assert react_unreact(data, user_admin.token, message_admin.message_id, 100, 'react') == {'ValueError': 'react_id is not a valid React ID'}


def test_react_good():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin = getting_message(data)[0]

    # React the message in advance
    # If the next text raises an exception means the react is successfully added
    output = react_unreact(data, user_admin.token, message_admin.message_id, 1, 'react')
    assert output == {}
    output = react_unreact(data, user_owner.token, message_admin.message_id, 1, 'react')
    assert output == {}
    output = react_unreact(data, user_in_channel.token, message_admin.message_id, 1, 'react')
    assert output == {}

    # React the message again see whether raise exception
    assert react_unreact(data, user_admin.token, message_admin.message_id, 1, 'react') == {'ValueError': 'user has reacted'}


def test_unreact_bad():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin = getting_message(data)[0]

    # react in advance
    react_unreact(data, user_admin.token, message_admin.message_id, 1, 'react')
    react_unreact(data, user_owner.token, message_admin.message_id, 1, 'react')
    react_unreact(data, user_in_channel.token, message_admin.message_id, 1, 'react')

    assert react_unreact(data, user_admin.token, 100, 1, 'unreact') == {'ValueError': 'Message (based on ID) no longer exists'}

    assert react_unreact(data, user_admin.token, message_admin.message_id, 100, 'unreact') == {
        'ValueError': 'react_id is not a valid React ID'}


def test_unreact_good():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin = getting_message(data)[0]

    # react in advance
    react_unreact(data, user_admin.token, message_admin.message_id, 1, 'react')
    react_unreact(data, user_owner.token, message_admin.message_id, 1, 'react')
    react_unreact(data, user_in_channel.token, message_admin.message_id, 1, 'react')

    # Unreact the message again see whether raise excepion
    output = react_unreact(data, user_admin.token, message_admin.message_id, 1, 'unreact')
    assert output == {}
    output = react_unreact(data, user_owner.token, message_admin.message_id, 1, 'unreact')
    assert output == {}
    output = react_unreact(data, user_in_channel.token, message_admin.message_id, 1, 'unreact')
    assert output == {}

    # React the message again see whether raise exception
    assert react_unreact(data, user_admin.token, message_admin.message_id, 1, 'unreact') == {'ValueError': 'user has not reacted'}
    assert react_unreact(data, user_owner.token, message_admin.message_id, 1, 'unreact') == {'ValueError': 'user has not reacted'}
    assert react_unreact(data, user_in_channel.token, message_admin.message_id, 1, 'unreact') == {'ValueError': 'user has not reacted'}


def test_pin_bad():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin = getting_message(data)[0]

    # Invalid input
    assert pin_unpin(data, user_admin.token, 100, 'pin') == {'ValueError': 'message_id is not a valid message'}

    assert pin_unpin(data, user_in_channel.token, message_admin.message_id, 'pin') == {'ValueError': 'The authorised user is not an admin'}

    assert pin_unpin(data, user_notin_channel.token, message_admin.message_id, 'pin') == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'}


def test_pin_good():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    message_admin = getting_message(data)[0]

    # Pin the message in advance, if the next test raise exception
    # means the message is successfully pinned
    output = pin_unpin(data, user_admin.token, message_admin.message_id, 'pin')
    assert output == {}

    assert pin_unpin(data, user_admin.token, message_admin.message_id, 'pin') == {"ValueError": "Message with ID message_id is already pinned"}


def test_unpin_bad():
    data = generate_data()
    user_admin, user_owner, user_in_channel, user_notin_channel = getting_user(data)
    channel = getting_channel(data)
    message_admin = getting_message(data)[0]

    # Invalid input
    assert pin_unpin(data, user_admin.token, 100, 'unpin') == {'ValueError': 'message_id is not a valid message'}

    assert pin_unpin(data, user_owner.token, message_admin.message_id, 'unpin') == {'ValueError': 'The authorised user is not an admin'}

    assert pin_unpin(data, user_notin_channel.token, message_admin.message_id, 'unpin') == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    assert pin_unpin(data, user_admin.token, message_admin.message_id, 'unpin') == {
        "ValueError": "Message with ID message_id is already unpinned"
    }

    # admin leave the channel
    ch_join_leave(data, user_admin.token, channel.channel_id, 'leave')
    assert pin_unpin(data, user_admin.token, message_admin.message_id, 'unpin') == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'}


def test_unpin_good():
    data = generate_data()
    user_admin = getting_user(data)[0]
    message_admin = getting_message(data)[0]

    # Pin the message in advance, if the next test raise exception
    # means the message is successfully pinned
    pin_unpin(data, user_admin.token, message_admin.message_id, 'pin')
    output = pin_unpin(data, user_admin.token, message_admin.message_id, 'unpin')
    assert output == {}
