#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Meilin
"""

from server.help import (find_channel, find_user, print_message)
from channel_class import Channel
from Data_class import Data
from user_class import User
from message_class import Message

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
    # check the existence of the auth user
    user = data.get_user('token', token)
    if user is None:
        return {'ValueError': 'The user is not exist'}
    # new channel data
    new_channel = Channel(channel_name, is_public, user.get_u_id())
    data.add_channel(new_channel)
    # return a channel id
    return {
        'channel_id': new_channel.get_channel_id()
    }


def ch_invite(data, token, u_id, channel_id):

    # check validation of channel id
    channel = data.get_channel(channel_id)
    if channel is None:
        return {'ValueError': 'Invalid channel id'}

    new_member = data.get_user('u_id', u_id)
    if new_member is None:
        return {'ValueError': 'Invalid u_id'}

    user_invite = data.get_user('token', token)
    if user_invite['u_id'] not in channel.get_user_list()        
        return {'AccessError': 'The authorised user is not already a member of\
 the channel'}

    if new_member['u_id'] in channel.get_user_list():
        return {'AccessError': 'The invite user is already a member of the \
channel'}

    # update the data, a new member added
    '''user_data = {
        'u_id': u_id,
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'is_owner': False
    }'''
    channel.join_invite_channel(new_member)
    return {}


def ch_details(data, token, channel_id):

    channel = data.get_channel(channel_id)
    # check validation of channel id
    if channel is None:
        return {'ValueError': 'Invalid channel id'}
    # check auth user is a member or not
    user = data.get_user('token', token)

    if user['u_id'] not in channel.get_user_list():
        return {'AccessError': 'User is not a member of Channel'}

    return {
        'name': channel.get_channel_name(),
        'owner_members': channel.get_owner_list(),
        'all_members': channel.get_user_list()
    }


def ch_leave(data, token, channel_id):
    # check validation of ch_id
    channel = data.get_channel(channel_id)
    if channel is None:
        return {'ValueError': 'Channel ID is invalid'}

    user = channel.get_user('token', token)
    # remove a list of that user's data
    channel.leave_channel(user)

    return {}


def ch_join(data, token, channel_id):
    # check validation of ch_id
    channel = data.get_channel(channel_id)
    if channel is None:
        return {'ValueError': 'Channel ID is invalid'}
    # check the channel is public or private
    # when the authorised user is not an admin
    user = data.get_user('token', token)
    if channel.get_is_public() is False and user['permission_id'] != 1:  # <---
        return {'AccessError': 'The channel is private'}
    # if the user is already a member of that channel
    if user['u_id'] in channel.get_user_list():
        return {'AccessError': 'Already a member of that channel'}
    # add a list of that user's data
    channel.join_invite_channel(user)
    return {}


def ch_addowner(data, token, channel_id, u_id):
    # check validation of the channel id
    channel = data.get_channel(channel_id)
    if channel is None:
        return {'ValueError': 'Invalid Channel ID'}
    '''user_list = channel['user_list']
    owner = is_owner(user_list, u_id)
    if owner is None:
    '''
    if u_id not in channel.get_user_list():
        return {'AccessError': 'Not a member of this channel'}
    # check the user is already the owner or not
    if u_id in channel.get_owner_list():
        return {'ValueError': 'User is already an owner of the channel'}

    # accesserror when the auth_user is not an owner of the slackr or channel
    user = data.get_user('token', token)
    # user_add = find_uid(data, u_id)
    # member_add = find_member(channel, user_add)
    # if user['permission_id'] == 3:
        # return {'AccessError': 'User is not an owner of the slackr or this \
# channel'}

    channel.add_owner(u_id)

    return {}


def ch_removeowner(data, token, channel_id, u_id):
    # check validation of the channel id
    channel = data.get_channel(channel_id)
    if channel is None:
        return {'ValueError': 'Invalid Channel ID'}

    # check the remove user is owner or not
    # if is_owner(channel['user_list'], u_id) is False:
    if u_id not in channel.get_owner_list():
        return {'ValueError': 'User is not an owner of the channel'}

    # accesserror when the auth_user is not an owner of the slackr or channel
    user = data.get_user('token', token)
    # owner = is_owner(channel['user_list'], user['u_id'])
    # if user['permission_id'] == 3 or owner is False:
    if user['u_id'] not in channel.get_owner_list():
        return {
            'AccessError': "User is not an owner of the slackr or this channel"
        }
    channel.remove_onwer(u_id)      # <--- is owner or not? make true or false?
    return {}


def ch_lists(data, token):
    user = data.get_user('token', token)
    return data.get_channel_list(user['u_id'])


def ch_listall(data, token):
    user = data.get_user('token', token)
    return data.get_channel_list_all(user['u_id'])


def fun_message(data, token, channel_id, start):
    user = data.get_user('token', token)
    channel = data.get_channel(channel_id)
    if channel is None:
        return {'ValueError': 'Channel ID is not a valid channel'}

    if user['u_id'] not in channel.get_user_list():
        return {'AccessError': 'when:  the authorised user has not joined the \
channel they are trying to post to'}
    message = data.get_message(1)   # is this correct? before there is a print function
    if start > len(message):
        return {'ValueError': 'start is greater than or equal to the total \
number of messages in the channel'}

    return data.get_channel_message(channel_id, start)
