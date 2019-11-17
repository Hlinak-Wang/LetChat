#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/10/15

@author: Meilin
"""

from server.channel_class import Channel
from server.helper import authorise, get_channel_message


# create a channel
@authorise
def ch_create(data, user, channel_name, is_public):
    # check is the channel name is valid
    if len(channel_name) > 20:
        return {'ValueError': 'The maximum characters of name is 20.'}
    # new channel data
    new_channel = Channel(channel_name, is_public, user.u_id)
    data.add_channel(new_channel)

    # return a channel id
    return {
        'channel_id': new_channel.channel_id
    }


@authorise
def ch_invite(data, user, u_id, channel_id):

    # check validation of channel id
    channel = data.get_element('channels_group', 'channel_id', channel_id)
    if channel is None:
        return {'ValueError': 'Invalid channel id'}

    new_member = data.get_element('users_group', 'u_id', u_id)
    if new_member is None:
        return {'ValueError': 'Invalid u_id'}

    if user.u_id not in channel.user_list:
        return {'AccessError': 'The authorised user is not already a member of\
 the channel'}

    if new_member.u_id in channel.user_list:
        return {'AccessError': 'The invite user is already a member of the \
channel'}

    # update the data, a new member added
    channel.join_invite_channel(new_member.u_id)
    return {}


@authorise
def ch_details(data, user, channel_id, host):

    channel = data.get_element('channels_group', 'channel_id', channel_id)
    # check validation of channel id
    if channel is None:
        return {'ValueError': 'Invalid channel id'}

    if user.u_id not in channel.user_list:
        return {'AccessError': 'User is not a member of Channel'}

    channelowner_list = []
    for uids in channel.owner_list:
            user = data.get_element('users_group', 'u_id', uids)
            member = user.get_user_detail('member', host)
            channelowner_list.append(member)

    channeluser_list = []
    for uids in channel.user_list:
            user = data.get_element('users_group', 'u_id', uids)
            member = user.get_user_detail('member', host)
            channeluser_list.append(member)

    return {
        'name': channel.channel_name,
        'owner_members': channelowner_list,
        'all_members': channeluser_list
    }


@authorise
def ch_join_leave(data, user, channel_id, action):
    # check validation of ch_id
    channel = data.get_element('channels_group', 'channel_id', channel_id)
    if channel is None:
        return {'ValueError': 'Channel ID is invalid'}
    if action == 'join':
        # check the channel is public or private
        # when the authorised user is not an admin
        if channel.is_public is False and user.permission_id != 1:
            return {'AccessError': 'The channel is private'}
        # if the user is already a member of that channel
        if user.u_id in channel.user_list:
            return {'AccessError': 'Already a member of that channel'}
        # add a list of that user's data
        channel.join_invite_channel(user.u_id)
    elif action == 'leave':
        # remove a list of that user's data
        channel.leave_channel(user.u_id)

    return {}


@authorise
def ch_add_remove_owner(data, user, channel_id, u_id, action):
    # check validation of the channel id
    channel = data.get_element('channels_group', 'channel_id', channel_id)
    if channel is None:
        return {'ValueError': 'Invalid Channel ID'}

    # if u_id is not a member of that channel
    if u_id not in channel.user_list:
        return {'AccessError': 'Not a member of this channel'}

    # accesserror when the auth_user is not an owner of the slackr or channel
    if user.permission_id == 3 and user.u_id not in channel.owner_list:
        return {'AccessError': 'User is not an owner of the slackr or this \
channel'}

    if action == 'add':
        # check the user is already the owner or not
        if u_id in channel.owner_list:
            return {'ValueError': 'User is already an owner of the channel'}

        channel.add_owner(u_id)

    elif action == 'remove':
        # check the remove user is owner or not
        if u_id not in channel.owner_list:
            return {'ValueError': 'User is not an owner of the channel'}

        channel.remove_owner(u_id)

    return {}


@authorise
def ch_lists_listall(data, user, action):

    channel_list = []
    for channel in data.channels_group:
        if action == 'lists' and user.u_id not in channel.user_list:
            continue
        if action == 'listall' \
                and not (channel.is_public or user.u_id in channel.user_list):
            continue

        channel_list.append({
            'name': channel.channel_name,
            'channel_id': channel.channel_id
        })

    return {
        'channels': channel_list
    }


@authorise
def fun_message(data, user, channel_id, start):
    channel = data.get_element('channels_group', 'channel_id', channel_id)
    if channel is None:
        return {'ValueError': 'Channel ID is not a valid channel'}

    if user.u_id not in channel.user_list:
        return {'AccessError': 'when:  the authorised user has not joined the \
channel they are trying to post to'}
    if start > data.get_earliest_index(channel_id):
        return {'ValueError': 'start is greater than or equal to the total \
number of messages in the channel'}

    return get_channel_message(data, channel_id, user.u_id, start)
