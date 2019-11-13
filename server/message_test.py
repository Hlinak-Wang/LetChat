#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from server.message_function import fun_send, message_operation, react_unreact, pin_unpin
from datetime import datetime, timedelta
from server.Data_class import Data
from server.auth_functions import register
from server.channel_function import ch_create, ch_join


# initial state of testing
def testdata():
    test_data = Data()
    user_chowner = register(test_data, 'test1@test.com', 'password', 'name_first1', 'name_last')
    user_inch = register(test_data, 'test2@test.com', 'password', 'name_first2', 'name_last')
    register(test_data, 'test3@test.com', 'password', 'name_first3', 'name_last')
    channel = ch_create(test_data, user_chowner['token'], 'test_channel', True)
    ch_join(test_data, user_inch['token'], channel['channel_id'])
    fun_send(test_data, user_inch['token'], channel['channel_id'], 'test2')
    fun_send(test_data, user_chowner['token'], channel['channel_id'], 'test')
    return test_data


def test_send_late():
    data = testdata()
    user = data.users_group[0]
    channel = data.channels_group[0]
    message_long = ""
    for i in range(0, 1010):
        message_long += "a"
    time_valid = datetime.now() + timedelta(seconds=10)
    time_invalid = datetime.now() - timedelta(seconds=10)
    # Invalid input
    assert fun_send(data, user.token, channel.channel_id, 'short', time_valid) == {'AccessError': 'User not exist'}

    assert fun_send(data, user.token, channel.channel_id, message_long, time_valid) == {
           "ValueError": "Message is more than 1000 characters"
    }
    assert fun_send(data, user.token, 1232, 'short_message', time_valid) == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'
    }

    assert fun_send(data, user.token, channel.channel_id, 'short_message', time_invalid) == {
        'ValueError': 'Time sent is a time in the past'
    }

    # Valid input
    output = fun_send(data, user.token, channel.channel_id, 'short_message', time_valid)
    assert output.u_id == user.u_id


def test_send():
    data = testdata()
    user = data.users_group[0]
    channel = data.channels_group[0]
    message_long = ""
    for i in range(0, 1010):
        message_long += "a"

    # Invalid input
    assert fun_send(data, user.token, channel.channel_id, message_long) == {
        "ValueError": "Message is more than 1000 characters"}

    assert fun_send(data, user.token, 2, 'short_message') == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'}

    # Valid input
    output = fun_send(data, user.token, channel.channel_id, 'short_message')
    assert output.u_id == user.u_id


def test_remove():
    data = testdata()
    user_admin = data.users_group[0]
    user_norm = data.users_group[1]
    message = data.messages_group[0]

    # Invalid input
    assert message_operation(data, user_norm.token, message.message_id) == {'AccessError': 'permission denied'}
    assert message_operation(data, user_norm.token, 100) == {'ValueError': 'Message (based on ID) no longer exists'}

    output = message_operation(data, user_admin.token, message.message_id)
    assert output == {}


def test_edit():
    data = testdata()
    user_admin = data.users_group[0]
    user_norm = data.users_group[1]
    message = data.messages_group[0]

    # Invalid input
    assert message_operation(data, user_norm.token, message.message_id, "new_message") == {'AccessError': 'permission denied'}
    assert message_operation(data, user_norm.token, 100, "new_message") == {
        'ValueError': 'Message (based on ID) no longer exists'}

    # Valid input
    output = message_operation(data, user_admin.token, message.message_id, "new_message")
    assert output == {}


def test_react():
    data = testdata()
    user = data.users_group[0]
    message = data.messages_group[0]

    # Invalid input
    assert react_unreact(data, user.token, 100, 1, 'react') == {'ValueError': 'Message (based on ID) no longer exists'}

    assert react_unreact(data, user.token, message.message_id, 100, 'react') == {'ValueError': 'react_id is not a valid React ID'}

    # React the message in advance
    # If the next text raises an exception means the react is successfully added
    output = react_unreact(data, user.token, message.message_id, 1, 'react')
    assert output == {}

    # React the message again see whether raise exception
    assert react_unreact(data, user.token, message.message_id, 1, 'react') == {'ValueError': 'user has reacted'}


def test_unreact():
    data = testdata()
    user = data.users_group[0]
    message = data.messages_group[0]

    # Invalid input
    assert react_unreact(data, user.token, 100, 1, 'react') == {'ValueError': 'Message (based on ID) no longer exists'}

    assert react_unreact(data, user.token, message.message_id, 100, 'react') == {
        'ValueError': 'react_id is not a valid React ID'}

    # React the message in advance
    # If the next text raises an exception means the react is successfully added
    output = react_unreact(data, user.token, message.message_id, 1, 'react')
    assert output == {}

    # Unreact the message again see whether raise excepion
    output = react_unreact(data, user.token, message.message_id, 1, 'unreact')
    assert output == {}

    # React the message again see whether raise exception
    assert react_unreact(data, user.token, message.message_id, 1, 'unreact') == {'ValueError': 'user has not reacted'}


def test_pin():
    data = testdata()
    user_admin = data.users_group[0]
    user_norm = data.users_group[1]
    user_not_in_channel = data.users_group[2]
    message = data.messages_group[0]

    # Invalid input
    assert pin_unpin(data, user_admin.token, 100, 'pin') == {'ValueError': 'message_id is not a valid message'}

    assert pin_unpin(data, user_norm.token, message.message_id, 'pin') == {'ValueError': 'The authorised user is not an admin'}

    assert pin_unpin(data, user_not_in_channel.token, message.message_id, 'pin') == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    # Pin the message in advance, if the next test raise exception
    # means the message is successfully pinned
    output = pin_unpin(data, user_admin.token, message.message_id, 'pin')
    assert output == {}

    assert pin_unpin(data, user_admin.token, message.message_id, 'pin') == {"ValueError": "Message with ID message_id is already pinned"}


def test_unpin():
    data = testdata()
    user_admin = data.users_group[0]
    user_norm = data.users_group[1]
    user_not_in_channel = data.users_group[2]
    message = data.messages_group[0]

    # Invalid input
    assert pin_unpin(data, user_admin.token, 100, 'unpin') == {'ValueError': 'message_id is not a valid message'}

    assert pin_unpin(data, user_norm.token, message.message_id, 'unpin') == {'ValueError': 'The authorised user is not an admin'}

    assert pin_unpin(data, user_not_in_channel.token, message.message_id, 'unpin') == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    assert pin_unpin(data, user_admin.token, message.message_id, 'unpin') == {"ValueError": "Message with ID message_id is already unpinned"}

    # Pin the message in advance, if the next test raise exception
    # means the message is successfully pinned
    pin_unpin(data, user_admin.token, message.message_id, 'unpin')
    output = pin_unpin(data, user_admin.token, message.message_id, 'unpin')
    assert output == {}
