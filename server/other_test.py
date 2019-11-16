#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from server.extra_function import message_search, permission_change, standup_message, standup_active, standup_begin
from server.auth_functions import register
from server.channel_function import ch_create, ch_join_leave
from server.message_function import fun_send, react_unreact
from datetime import datetime, timedelta, timezone
from server.Data_class import Data


def get_data():
    test_data = Data()
    user_chowner = register(test_data, 'test1@test.com', 'password', 'name_first1', 'name_last')
    user_inch = register(test_data, 'test2@test.com', 'password', 'name_first2', 'name_last')
    register(test_data, 'test3@test.com', 'password', 'name_first3', 'name_last')
    channel = ch_create(test_data, user_chowner['token'], 'test_channel', True)
    ch_join_leave(test_data, user_inch['token'], channel['channel_id'], 'join')
    message_inch = fun_send(test_data, user_inch['token'], channel['channel_id'], 'test2')
    message_chowner = fun_send(test_data, user_chowner['token'], channel['channel_id'], 'test')
    react_unreact(test_data, user_inch['token'], message_inch['message_id'], 1, 'react')
    react_unreact(test_data, user_inch['token'], message_chowner['message_id'], 1, 'react')
    ch_create(test_data, user_chowner['token'], 'test_channel2', True)
    return test_data


def test_standup_start():

    data = get_data()
    user = data.users_group[0]
    user_notch = data.users_group[2]
    channel = data.channels_group[0]
    
    # Invalid input
    assert fun_standup_star(data, user.token, -123) == {
        'ValueError': 'Channel ID is not a valid channel'
    }

    assert fun_standup_star(data, user_notch.token, channel.channel_id) == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'
    }

    output = fun_standup_star(data, user.token, channel.channel_id)
    time_finish = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 900
    assert time_finish - 1 <= output['time_finish'] <= time_finish + 1

    # Start standup again
    assert fun_standup_star(data, user.token, channel.channel_id) == {
        'ValueError': 'An active standup is currently running in this channel'
    }


def test_standup_send():
    data = get_data()
    user = data.users_group[0]
    user_notch = data.users_group[2]
    channel = data.channels_group[0]
    channel2 = data.channels_group[1]

    message_long = ''
    for i in range(0, 1010):
        message_long += '1'
    
    # Test in the environment of standup has started
    fun_standup_star(data, user.token, channel.channel_id)
    
    # Testing invalid input
    assert fun_standup_send(data, user.token, -123, 'message_short') == {
        'ValueError': 'Channel ID is not a valid channel'
    }

    assert fun_standup_send(data, user.token, channel.channel_id, message_long) == {
        'ValueError': 'Message is more than 1000 characters'
    }

    assert fun_standup_send(data, user_notch.token, channel.channel_id, 'message_short') == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'
    }

    assert fun_standup_send(data, user_notch.token, channel2.channel_id, 'message_short') == {
        'ValueError': 'An active standup is not currently running in this channel'
    }

    fun_standup_send(data, user.token, channel.channel_id, 'message_short')
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
    channel = data.channels_group[0]

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
