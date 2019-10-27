#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""


# find user by token, return user if found, return None if not found
def find_user(data, token):
    for user in data['users']:
        if user['token'] == token:
            return user

    return None


# find user by channel_id, return channel if found, return None if not found
def find_channel(data, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    return None


# find message by message_id, return message if found, return None if not found
def find_message_channel(data, message_id):
    for channel in data['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return message, channel

    return None, None


# find owner in user_list, return user if found
def find_ownership(user_list, member):
    for user in user_list:
        if user['u_id'] == member['u_id']:
            return user['is_owner']


# find react by react_id, return react if found, return None if not found
def find_react(react_list, react_id):
    for react in react_list:
        if react['react_id'] == react_id:
            return react
    return None
