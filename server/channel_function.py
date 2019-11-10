#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Meilin
"""

from datetime import datetime, timezone
from server.help import find_channel, find_user, print_message


def find_uid(data, u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return user
    return None


def is_owner(user_list, u_id):
    for user in user_list:
        if user['u_id'] == u_id:
            return user['is_owner']
    return None


def find_member(channel, user):
    for member in channel['user_list']:
        if member['u_id'] == user['u_id']:
            return member

    return None


# create a channel
def ch_create(data, token, channel_name, is_public):
    # check is the channel name is valid
    if len(channel_name) > 20:
        return {'ValueError': 'The maximum characters of name is 20.'}
    user = find_user(data, token)
    if user is None:
        return {'ValueError': 'The user is not exist'}
    channel_id = len(data['channels'])
    # assume channel_data
    channel_data = {
        'name': channel_name,
        'channel_id': channel_id,
        'user_list': [
            {
                'u_id': user['u_id'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'is_owner': True
            }
        ],
        'is_public': is_public,
        'messages': [],
        'standup_queue': [],
        'standup': {'time_finish': '1/1/1900, 1:00:00', 'u_id': None},
        'standup_message': ''
    }
    data['channels'].append(channel_data)
    user['channel_involve'].append(channel_id)
    # return a channel id
    return {
        'channel_id': channel_id
    }


def ch_invite(data, token, u_id, channel_id):

    # check validation of channel id
    channel = find_channel(data, channel_id)
    if channel is None:
        return {'ValueError': 'Invalid channel id'}

    user = find_uid(data, u_id)
    if user is None:
        return {'ValueError': 'Invalid u_id'}

    user_invite = find_user(data, token)
    if find_member(channel, user_invite) is None:
        return {'AccessError': 'The authorised user is not already a member of\
 the channel'}

    if find_member(channel, user) is not None:
        return {'AccessError': 'The invite user is already a member of the \
channel'}

    # update the data, a new member added
    user_data = {
        'u_id': u_id,
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'is_owner': False
    }
    channel['user_list'].append(user_data)
    user['channel_involve'].append(channel_id)
    return {}


def ch_details(data, token, channel_id):

    channel = find_channel(data, channel_id)
    # check validation of channel id
    if channel is None:
        return {'ValueError': 'Invalid channel id'}
    # check auth user is a member or not
    user = find_user(data, token)

    if find_member(channel, user) is None:
        return {'AccessError': 'User is not a member of Channel'}

    owner_members = []
    all_members = []
    for member in channel['user_list']:
        all_members.append({
            'u_id': member['u_id'],
            'name_first': member['name_first'],
            'name_last': member['name_last']
        })

        if member['is_owner']:
            owner_members.append({
                'u_id': member['u_id'],
                'name_first': member['name_first'],
                'name_last': member['name_last']
            })

    return {
        'name': channel['name'],
        'owner_members': owner_members,
        'all_members': all_members
    }


def ch_leave(data, token, channel_id):

    user = find_user(data, token)

    # check validation of ch_id
    channel = find_channel(data, channel_id)
    if channel is None:
        return {'ValueError': 'Channel ID is invalid'}

    # remove a list of that user's data
    member = find_member(channel, user)
    channel['user_list'].remove(member)
    user['channel_involve'].remove(channel_id)

    return {}


def ch_join(data, token, channel_id):
    # check validation of ch_id
    channel = find_channel(data, channel_id)
    if channel is None:
        return {'ValueError': 'Channel ID is invalid'}
    # check the channel is public or private
    # when the authorised user is not an admin
    user = find_user(data, token)
    if channel['is_public'] is False and user['permission_id'] != 1:
        return {'AccessError': 'The channel is private'}
    # if the user is already a member of that channel
    if find_member(channel, user) is not None:
        return {'AccessError': 'Already a member of that channel'}
    # add a list of that user's data
    user = find_user(data, token)
    user_data = {
        'u_id': user['u_id'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'is_owner': False
    }
    channel['user_list'].append(user_data)
    user['channel_involve'].append(channel_id)
    return {}


def ch_addowner(data, token, channel_id, u_id):
    # check validation of the channel id
    channel = find_channel(data, channel_id)
    if channel is None:
        return {'ValueError': 'Invalid Channel ID'}
    user_list = channel['user_list']
    owner = is_owner(user_list, u_id)
    if owner is None:
        return {'AccessError': 'Not a member of this channel'}
    # check the user is already the owner or not
    if is_owner(channel['user_list'], u_id) is True:
        return {'ValueError': 'User is already an owner of the channel'}

    # accesserror when the auth_user is not an owner of the slackr or channel
    user = find_user(data, token)
    user_add = find_uid(data, u_id)
    member_add = find_member(channel, user_add)
    if user['permission_id'] == 3:
        return {'AccessError': 'User is not an owner of the slackr or this \
channel'}

    makeowner = find_member(channel, member_add)
    makeowner['is_owner'] = True

    return {}


def ch_removeowner(data, token, channel_id, u_id):
    # check validation of the channel id
    channel = find_channel(data, channel_id)
    if channel is None:
        return {'ValueError': 'Invalid Channel ID'}

    # check the user is owner or not
    if is_owner(channel['user_list'], u_id) is False:
        return {'ValueError': 'User is not an owner of the channel'}

    # accesserror when the auth_user is not an owner of the slackr or channel
    user = find_user(data, token)
    owner = is_owner(channel['user_list'], user['u_id'])
    if user['permission_id'] == 3 or owner is False:
        return {
            'AccessError': "User is not an owner of the slackr or this channel"
        }
    user_move = find_uid(data, u_id)
    removeowner = find_member(channel, user_move)
    removeowner['is_owner'] = False
    return {}


def ch_lists(data, token):
    user = find_user(data, token)
    ch_id = user['channel_involve']
    stack_channel = []
    for channel in data['channels']:
        for i in ch_id:
            if channel['channel_id'] == i:
                stack_channel.append({
                    'name': channel['name'],
                    'channel_id': channel['channel_id']
                })

    return {
        'channels': stack_channel
    }


def ch_listall(data, token):
    user = find_user(data, token)
    stack_channel = []
    for channel in data['channels']:
        if channel['is_public']:
            stack_channel.append({
                                'name': channel['name'],
                                'channel_id': channel['channel_id']
                                })
        elif not channel['is_public']:
            if find_member(channel, user) is not None:
                stack_channel.append({
                    'name': channel['name'],
                    'channel_id': channel['channel_id']
                                })
    return {
        'channels': stack_channel
    }


def fun_message(data, token, channel_id, start):
    output_list = []
    user = find_user(data, token)
    channel = find_channel(data, channel_id)
    if channel is None:
        return {'ValueError': 'Channel ID is not a valid channel'}

    if channel_id not in user['channel_involve']:
        return {'AccessError': 'when:  the authorised user has not joined the \
channel they are trying to post to'}

    if start > len(channel['messages']):
        return {'ValueError': 'start is greater than or equal to the total \
number of messages in the channel'}

    end = start
    for message in channel['messages'][start:]:
        print_message(user, message, output_list)
        end += 1
        if end >= start + 50:
            return {
                'messages': output_list,
                'start': start,
                'end': end
            }

    return {
        'messages': output_list,
        'start': start,
        'end': -1
    }
