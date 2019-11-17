#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Eric
"""

from datetime import datetime
from server.message_class import Message
from server.helper import authorise


# Send a message from authorised_user to the channel specified by channel_id
@authorise
def send_message(data, user, channel_id, message, time_create=0):

    time_now = datetime.now().timestamp()
    if time_create == 0:
        time_create = time_now

    if len(message) > 1000:
        return {"ValueError": "Message is more than 1000 characters"}

    channel = data.get_channel(channel_id)

    if channel is None or user.u_id not in channel.user_list:
        return {'AccessError': 'the authorised user has not joined the channel they are trying to post to'}

    if time_create < time_now:
        return {"ValueError": 'Time sent is a time in the past'}

    new_message = Message(message, channel_id, user.u_id, time_create)
    data.message_operation(new_message, 'add')
    return {'message_id': new_message.message_id}


# remove or edit a message
@authorise
def message_operation(data, user, message_id, message_edit=""):

    message = data.get_message(message_id)
    if message is None:
        return {'ValueError': 'Message (based on ID) no longer exists'}

    channel = data.get_channel(message.channel_id)

    if user.u_id in channel.owner_list:
        is_owner = True
    else:
        is_owner = False

    if user.u_id != message.u_id:
        if not is_owner or user.permission_id == 3:
            return {
                'AccessError': 'permission denied'
            }

    if message_edit == "":
        data.message_operation(message, 'remove')
    else:
        message.user_edit(message_edit)

    return {}


@authorise
def react_unreact(data, user, message_id, react_id, action):

    message = data.get_message(message_id)
    if message is None:
        return {'ValueError': 'Message (based on ID) no longer exists'}

    react = message.get_react_by_id(react_id)

    if react is None:
        return {'ValueError': 'react_id is not a valid React ID'}

    if action == 'react':
        if user.u_id in react.u_ids:
            return {'ValueError': 'user has reacted'}
        react.user_react(user.u_id)

    elif action == 'unreact':
        if user.u_id not in react.u_ids:
            return {'ValueError': 'user has not reacted'}
        react.user_unreact(user.u_id)

    return {}


@authorise
def pin_unpin(data, user, message_id, action):

    message = data.get_message(message_id)
    if message is None:
        return {'ValueError': 'message_id is not a valid message'}

    channel = data.get_channel(message.channel_id)
    if channel is None or user.u_id not in channel.user_list:
        return {'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    if user.permission_id == 3:
        return {'ValueError': 'The authorised user is not an admin'}

    if action == 'pin':
        if message.is_pinned:
            return {"ValueError": "Message with ID message_id is already pinned"}
        message.user_pin()

    elif action == 'unpin':
        if not message.is_pinned:
            return {"ValueError": "Message with ID message_id is already unpinned"}
        message.user_unpin()

    return {}
