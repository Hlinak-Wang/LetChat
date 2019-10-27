#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from server.extra_function import message_search, fun_standup_send, fun_standup_star, permission_change
from server.auth_functions import register
from server.channel_function import ch_create, ch_join
from server.message_function import fun_send, fun_react
from datetime import datetime, timedelta

def getData():
    data = {
        'users': [],
        'channels': [],
        'message_counter': 0,
        'message_buffer': []
    }
    user_chowner = register(data, 'test1@test.com', 'password', 'name_first1', 'name_last')
    user_inch = register(data, 'test2@test.com', 'password', 'name_first2', 'name_last')
    register(data, 'test3@test.com', 'password', 'name_first3', 'name_last')
    channel = ch_create(data, user_chowner['token'], 'test_channel', True)
    ch_join(data, user_inch['token'], channel['channel_id'])
    fun_send(data, user_inch['token'], channel['channel_id'], 'test2')
    fun_send(data, user_chowner['token'], channel['channel_id'], 'test')
    fun_react(data, user_inch['token'], 0, 1)
    fun_react(data, user_inch['token'], 1, 1)
    ch_create(data, user_chowner['token'], 'test_channel2', True)
    return data


def test_standup_start():
    
    data = getData()
    user = data['users'][0]
    user_notch = data['users'][2]
    channel = data['channels'][0]

    channel_not_exist = 199
    
    # Invalid input
    assert fun_standup_star(data, user['token'], channel_not_exist) == {
        'ValueError': 'Channel ID is not a valid channel'
    }

    assert  fun_standup_star(data, user_notch['token'], channel['channel_id']) == {
        'AccessError': 'The authorised user is not a member of the channel that the message is within'
    }

    output = fun_standup_star(data, user['token'], channel['channel_id'])

    assert output['time_finish'] == datetime.strftime(datetime.now() + timedelta(seconds=900), "%m/%d/%Y, %H:%M:%S")

    # Start standup again
    assert fun_standup_star(data, user['token'], channel['channel_id']) == {
        'ValueError': 'An active standup is currently running in this channel'
    }


def test_standup_send():

    data = getData()
    user = data['users'][0]
    user_notch = data['users'][2]
    channel = data['channels'][0]
    channel2 = data['channels'][1]
    
    channel_not_valid = 100
    message_long = ''
    for i in range(0, 1010):
        message_long += '1'
    
    # Test in the environment of standup has started
    fun_standup_star(data, user['token'], channel['channel_id'])
    
    # Testing invalid input
    assert fun_standup_send(data, user['token'], channel_not_valid, 'message_short') == {
        'ValueError': 'Channel ID is not a valid channel'
    }

    assert fun_standup_send(data, user['token'], channel['channel_id'], message_long) == {
        'ValueError': 'Message is more than 1000 characters'
    }

    assert fun_standup_send(data, user_notch['token'], channel['channel_id'], 'message_short') == {
        'AccessError': 'the authorised user has not joined the channel they are trying to post to'
    }

    assert fun_standup_send(data, user_notch['token'], channel2['channel_id'], 'message_short') == {
        'ValueError': 'An active standup is not currently running in this channel'
    }

    fun_standup_send(data, user['token'], channel['channel_id'], 'message_short')
    assert channel['standup_queue'][0]['message'] == 'message_short'

def test_search():

    data = getData()
    user = data['users'][0]
    
    # No message match
    output = message_search(data, user['token'], "No message match")
    assert output['messages'] == []
    
    # One message match
    output = message_search(data, user['token'], "test")
    assert len(output['messages']) == 1
    assert output['messages'][0]['message_id'] == 1


def test_userpermission_change():

    data = getData()
    user = data['users'][0]
    user_norm1 = data['users'][2]
    user_norm2 = data['users'][1]
    channel = data['channels'][0]
    
    u_id_not_valid = -100000
    out = permission_change(data, user['token'], user_norm1['u_id'], 2)
    assert user_norm1['permission_id'] == 2

    # invalid input
    assert permission_change(data, user['token'], u_id_not_valid, 2) == {
        'ValueError': 'u_id does not refer to a valid user'
    }

    assert permission_change(data, user['token'], user_norm1['u_id'], 4) == {
        'ValueError': 'permission_id does not refer to a value permission'
    }

    assert permission_change(data, user_norm2['token'], user_norm1['u_id'], 2) == {
        'AcessError': 'The authorised user is not an admin or owner'
    }
