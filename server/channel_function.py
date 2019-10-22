from flask import Flask, request
from json import dumps

'''
class Channel:
    def __init__(self, name, is_public, u_id, channel_id):
        self.name = name
        self.is_public = is_public
        self.u_id = u_id
        self.channel_id = channel_id
    def get_name(self):
        return self.name
    def get_state_of_channel(self):
        return self.is_public
    def get_u_id(self):
        return self.u_id
    def get_channel_id(self):
        return self.channel_id
'''   


def find_user(data, token):
    for user in data['users']:
        if user['token'] == token:
            return user
    return None


def find_uid(data, u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return user
    return None


def find_channel_name(data, channel_id):
    for name in data['channels']:
        if name['channel_id'] == channel_id:
            return name['name']
    return None


def find_ownership(user_list):
    owner_member = []
    for owner in user_list:
        if owner[is_owner]:
            owner_member.append(owner['u_id'])
    return owner_member


def is_owner(user_list, member):
    for user in user_list:
        if user['u_id'] == member['u_id']:
            return user['is_owner']
    return None


def find_channel(data, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    return None


def find_member(channel, user):
    for member in channel['user_list']:
        if member['u_id'] == user['u_id']:
            return member

    return None


# create a channel
def ch_create(data, token, channel_name, is_public):

    user = find_user(data, token)

    # check is the channel name is valid
    if len(channel_name) > 20:
        raise ValueError('The maximum characters of name is 20.')
        
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
        'is_public': is_public
    }

    data['channels'].append(channel_data)
    
    # return a channel id
    return {
        'channel_id': channel_id
    }


def ch_invite(data, token, u_id, channel_id):

    channel = find_channel(data, channel_id)
    # check validation of channel id
    if channel is None:
        raise ValueError('Invalid channel id')

    user_invite = find_user(data, token)
    if find_member(channel, user_invite) is None:
        raise ValueError('Invalid channel id')

    user = find_uid(data, u_id)
    if user is None:
        raise ValueError('Invalid u_id')

    if find_member(channel, user) is not None:
        raise Exception('the authorised user is not already a member of the channel')
    
    # update the data, a new member added
    user_data = {
        'u_id': u_id,
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'is_owner': False
    }
    channel['user_list'].append(user_data)
    return {}


def ch_details(data, token, channel_id):

    channel = find_channel(data, channel_id)
    # check validation of channel id
    if channel is None:
        raise ValueError('Invalid channel')
    # check auth user is a member or not
    user = find_user(data, token)

    if find_member(data, user) is None:
        raise Exception('Not a member of that channel')

    channel = find_channel(data, channel_id)
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

'''
def ch_message():
    return dumps({})
'''

def ch_leave():
    detail = get_channels(data)
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    # check validation of ch_id
    channel = find_channel(Data, channel_id)
    if channel is None:
        raise ValueError('Channel ID is invalid')
    
    user = find_user(Data, token)
    # remove a list of that user's data
    member = find_member(channel, user)
    if user != None:
        channel['user_list'].remove(member)
        user['channel_involve'].remove(channel_id)
    
    return {}

def ch_join():

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    # check validation of ch_id
    channel = find_channel(Data, channel_id)
    if channel == None:
        raise ValueError('Channel ID is invalid')
    # check the channel is public or private
    # when the authorised user is not an admin
    user = find_user(Data, token)
    if channel['is_public'] is False and user['permission_id'] != 1:
        raise AccessError('The channel is private')
    
    # add a list of that user's data
    user = find_user(Data, token)
    if user is not None:
        user_data = {
            'u_id': user['u_id'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
        }
        channel['user_list'].append(user_data)
    return {}
    
def ch_addowner():

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    detail = get_channels(Data)
    
    # check validation of the channel id
    channel = find_channel(Data, channel_id)
    if channel is None:
        raise ValueError('Invalid Channel ID')
        
    # check the user is already the owner or not
    if is_owner(channel['user_list'], u_id) is True:
        raise ValueError('Already an owner of that channel')
        
    # accesserror when the auth_user is not an owner of the slackr or channel
    user = find_user(Data, token)
    owner = is_owner(channel['user_list'], user['u_id'])
    if user is not None:
        if user['permission_id'] == 3 or owner is False:
            raise AccessError("User is not an owner of the slackr or this channel")
    
    owner = find_uid_in_channel(detail, channel_id, u_id)
    if owner is not None:
        uid['is_owner'] = True
    
    return {}
    
def ch_removeowner():

    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    detail = get_channels(Data)
    
    # check validation of the channel id
    channel = find_channel(Data, channel_id)
    if channel is None:
        raise ValueError('Invalid Channel ID')
        
    # check the user is owner or not
    if is_owner(channel['user_list'], u_id) is False:
        raise ValueError('Not an owner')
    
    # accesserror when the auth_user is not an owner of the slackr or channel
    user = find_user(Data, token)
    owner = is_owner(channel['user_list'], user['u_id'])
    if user is not None:
        if user['permission_id'] == 3 or owner is False:
            raise AccessError("User is not an owner of the slackr or this channel")
    
    owner = find_uid_in_channel(detail, channel_id, u_id)
    if owner is not None:
        uid['is_owner'] = False
    return {}
    
def ch_lists():

    detail = get_channels(Data)
    token = request.args.get('token')
    user = find_user(Data, token)
    if user is not None:
        ch_id = user['channel_involve']
    
    stack_channel = []
    for channel in detail:
        for i in ch_id:
            if channel['channel_id'] == i:
                stack_channel.append({
                                    'name': channel['name'],
                                    'channel_id': channel['channel_id']    
                                    })
    return {stack_channel}
    
def ch_listall():

    detail = get_channels(Data)
    token = request.args.get('token')
    stack_channel = []
    for channel in detail:
        if channel['is_public'] == True:
            stack_channel.append({
                                'name': channel['name'],
                                'channel_id': channel['channel_id']    
                                })
    return {stack_channel}
    

