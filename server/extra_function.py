#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from datetime import datetime
from server.message_function import send_message
from server.helper import authorise


@authorise
def message_search(data, user, query_str):

    channel_join = data.get_channels_joined(user.u_id)
    output_list = []
    for message in data.messages_group:
        time_now = datetime.now().timestamp()
        if message.channel_id in channel_join and message.time_created <= time_now:
            if message.message == query_str:
                output_list.append(message.get_message_info(user.u_id))

    return {
        'messages': output_list
    }


@authorise
def permission_change(data, user, u_id, permission_id):

    if user.permission_id == 3:
        return {'AcessError': 'The authorised user is not an admin or owner'}

    target = data.get_element('users_group', 'u_id', u_id)
    if target is None:
        return {'ValueError': 'u_id does not refer to a valid user'}

    if permission_id not in range(1, 4):
        return {'ValueError': 'permission_id does not refer to a value permission'}

    target.set_permission_id(permission_id)
    return {}


@authorise
def standup_begin(data, user, channel_id, length):

    channel = data.get_element('channels_group', 'channel_id', channel_id)
    time_start = datetime.now().timestamp()

    if channel is None:
        return {'ValueError': 'Channel ID is not a valid channel'}

    if user.u_id not in channel.user_list:
        return {'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    if time_start < channel.standup['time_finish']:
        return {'ValueError': 'An active standup is currently running in this channel'}

    channel.set_standup(time_start + length, user.u_id)

    return {
        'time_finish': channel.standup['time_finish']
    }


@authorise
def standup_active(data, user, channel_id):

    channel = data.get_element('channels_group', 'channel_id', channel_id)
    time_now = datetime.now().timestamp()
    if channel.standup['time_finish'] < time_now:
        is_activate = False
    else:
        is_activate = True

    user_beginer = data.get_element('users_group', 'u_id', channel.standup['u_id'])
    if not is_activate and channel.standup_message != '':
        send_message(data, user_beginer.token, channel_id, channel.standup_message)
        channel.standup_message = ''

    return {
        'is_activate': is_activate,
        'time_finish': channel.standup['time_finish']
    }


@authorise
def standup_message(data, user, channel_id, message):

    channel = data.get_element('channels_group', 'channel_id', channel_id)
    time_now = datetime.now().timestamp()
    if channel is None:
        return {'ValueError': 'Channel ID is not a valid channel'}

    if time_now > channel.standup['time_finish']:
        return {'ValueError': 'An active standup is not currently running in this channel'}

    if len(message) > 1000:
        return {'ValueError': 'Message is more than 1000 characters'}

    if user.u_id not in channel.user_list:
        return {'AccessError': 'the authorised user has not joined the channel they are trying to post to'}

    channel.standup_send(message)

    return {}

