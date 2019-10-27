#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from server.message_function import fun_send_late, fun_send, fun_remove, fun_edit, fun_react, fun_unreact, fun_pin, \
    fun_unpin
from server.auth_functions import register
from server.channel_function import ch_create, ch_join

# initial state of testing
def getdata():
    data = {
        'users': [],
        'channels': [],
        'message_counter': 0,
        'message_buffer': []
    }
    user_chowner = register(data, 'test1@test.com', 'password', 'name_first1', 'name_last')
    user_inch = register(data, 'test2@test.com', 'password', 'name_first2', 'name_last')
    user_notch = register(data, 'test3@test.com', 'password', 'name_first3', 'name_last')
    channel = ch_create(data, user_chowner['token'], 'test_channel', True)
    ch_join(data, user_inch['token'], channel['channel_id'])
    fun_send(data, user_inch['token'], channel['channel_id'], 'test2')
    fun_send(data, user_chowner['token'], channel['channel_id'], 'test')
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
    assert output == {'message_id': 2}

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
    assert output == {'message_id': 2}
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
