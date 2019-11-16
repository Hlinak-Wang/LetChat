#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from server.extra_function import message_search, permission_change, standup_message, standup_active, standup_begin
from server.auth_functions import register
from server.channel_function import ch_create, ch_join_leave
from server.message_function import send_message, react_unreact
from datetime import datetime
from server.Data_class import Data


def get_data():
    test_data = Data()
    user_chowner = register(test_data, 'test1@test.com', 'password', 'name_first1', 'name_last')
    user_inch = register(test_data, 'test2@test.com', 'password', 'name_first2', 'name_last')
    register(test_data, 'test3@test.com', 'password', 'name_first3', 'name_last')
    channel = ch_create(test_data, user_chowner['token'], 'test_channel', True)
    ch_join_leave(test_data, user_inch['token'], channel['channel_id'], 'join')
    message_inch = send_message(test_data, user_inch['token'], channel['channel_id'], 'test2')
    message_chowner = send_message(test_data, user_chowner['token'], channel['channel_id'], 'test')
    react_unreact(test_data, user_inch['token'], message_inch['message_id'], 1, 'react')
    react_unreact(test_data, user_inch['token'], message_chowner['message_id'], 1, 'react')
    ch_create(test_data, user_chowner['token'], 'test_channel2', True)
    return test_data


def test_standup_start():
    data = get_data()
    user = data.users_group[0]
    user_notch = data.users_group[2]
    channel = data.channels_group[0]
    length = 100
    # Invalid input
    assert standup_begin(data, user.token, -123, length) == {
        'ValueError': 'Channel ID is not a valid channel'
    }

    assert standup_begin(data, user_notch.token, channel.channel_id, length) == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'
    }

    output = standup_begin(data, user.token, channel.channel_id, length)
    time_finish = datetime.now().timestamp() + length
    assert time_finish - 1 <= output['time_finish'] <= time_finish + 1

    # Start standup again
    assert standup_begin(data, user.token, channel.channel_id, length) == {
        'ValueError': 'An active standup is currently running in this channel'
    }


def test_standup_active():
    data = get_data()
    user = data.users_group[0]
    user_notch = data.users_group[2]
    channel = data.channels_group[0]

    assert standup_active(data, user.token, channel.channel_id)['is_activate'] == False

    # start a standup
    length = 10
    output = standup_begin(data, user.token, channel.channel_id, length)
    assert standup_active(data, user.token, channel.channel_id)['is_activate'] == True
    assert standup_active(data, user.token, channel.channel_id)['time_finish'] == output['time_finish']


def test_standup_send():
    data = get_data()
    user = data.users_group[0]
    user_notch = data.users_group[2]
    channel = data.channels_group[0]
    channel2 = data.channels_group[1]
    length = 100
    message_long = ''
    for i in range(0, 1010):
        message_long += '1'

    # Test in the environment of standup has started
    standup_begin(data, user.token, channel.channel_id, length)

    # Testing invalid input
    assert standup_message(data, user.token, -123, 'message_short') == {
        'ValueError': 'Channel ID is not a valid channel'
    }

    assert standup_message(data, user.token, channel.channel_id, message_long) == {
        'ValueError': 'Message is more than 1000 characters'
    }

    assert standup_message(data, user_notch.token, channel.channel_id, 'message_short') == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'
    }

    assert standup_message(data, user_notch.token, channel2.channel_id, 'message_short') == {
        'ValueError': 'An active standup is not currently running in this channel'
    }

    standup_message(data, user.token, channel.channel_id, 'message_short')
    assert channel.standup_message == 'message_short\n'


def test_search():
    data = get_data()
    user = data.users_group[0]

    # No message match
    output = message_search(data, user.token, "No message match")
    assert output['messages'] == []

    # One message match
    output = message_search(data, user.token, "test")
    assert len(output['messages']) == 1
    assert output['messages'][0]['message'] == 'test'


def test_userpermission_change():
    data = get_data()
    user = data.users_group[0]
    user_norm1 = data.users_group[2]
    user_norm2 = data.users_group[1]

    out = permission_change(data, user.token, user_norm1.u_id, 2)
    assert user_norm1.permission_id == 2

    # invalid input
    assert permission_change(data, user.token, -123, 2) == {
        'ValueError': 'u_id does not refer to a valid user'
    }

    assert permission_change(data, user.token, user_norm1.u_id, 4) == {
        'ValueError': 'permission_id does not refer to a value permission'
    }

    assert permission_change(data, user_norm2.token, user_norm1.u_id, 2) == {
        'AcessError': 'The authorised user is not an admin or owner'
    }
