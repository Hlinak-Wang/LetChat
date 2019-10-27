#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from datetime import datetime, timedelta
from server.help import find_channel, find_user


def message_search(data, token, query_str):
    user = find_user(data, token, 'token')

    channel_join_list = []
    for channel_join in user['channel_involve']:
        channel_join_list.append(find_channel(data, channel_join))

    output_list = []
    for channel in channel_join_list:
        for message in channel['messages']:
            if message['message'] == query_str:
                react_list = message['reacts']
                for react in react_list:
                    if user['u_id'] in react['u_ids']:
                        react['is_this_user_reacted'] = True
                    else:
                        react['is_this_user_reacted'] = False

                output_list.append({
                    'message_id': message['message_id'],
                    'u_id': message['u_id'],
                    'message': message['message'],
                    'time_created': message['time_created'],
                    'reacts': react_list,
                    'is_pinned': message['is_pinned']
                })

    return {
        'messages': output_list,
    }


def permission_change(data, token, u_id, permission_id):
    user = find_user(data, token, 'token')

    if user['permission_id'] == 3:
        return {'AcessError': 'The authorised user is not an admin or owner'}

    target = find_user(data, u_id, 'u_id')
    if target is None:
        return {'ValueError': 'u_id does not refer to a valid user'}

    if permission_id not in range(1, 4):
        return {'ValueError': 'permission_id does not refer to a value permission'}

    target['permission_id'] = permission_id
    print(target)
    return {}


def fun_standup_star(data, token, channel_id):
    user = find_user(data, token, 'token')
    channel = find_channel(data, channel_id)

    if channel is None:
        return {'ValueError': 'Channel ID is not a valid channel'}

    if channel_id not in user['channel_involve']:
        return {'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    if datetime.now() < datetime.strptime(channel['standup']['time_finish'], "%m/%d/%Y, %H:%M:%S"):
        return {'ValueError': 'An active standup is currently running in this channel'}

    channel['standup']['time_finish'] = datetime.strftime(datetime.now() + timedelta(seconds=900), "%m/%d/%Y, %H:%M:%S")
    channel['standup']['u_id'] = user['u_id']

    return {
        'time_finish': channel['standup']['time_finish']
    }


def fun_standup_send(data, token, channel_id, message):

    user = find_user(data, token, 'token')
    channel = find_channel(data, channel_id)

    if channel is None:
        return {'ValueError': 'Channel ID is not a valid channel'}

    if datetime.now() > datetime.strptime(channel['standup']['time_finish'], "%m/%d/%Y, %H:%M:%S"):
        return {'ValueError': 'An active standup is not currently running in this channel'}

    if len(message) > 1000:
        return {'ValueError': 'Message is more than 1000 characters'}

    if channel_id not in user['channel_involve']:
        return {'AccessError': 'the authorised user has not joined the channel they are trying to post to'}

    channel['standup_queue'].append({
        'u_id': user['u_id'],
        'message_id': data['message_counter'],
        'message': message,
        'time_created': datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S"),
        'reacts': [{'react_id': 1, 'u_ids': []}],
        'is_pinned': False,
    })

    return {}

