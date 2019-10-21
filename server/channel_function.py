from flask import Flask, request
from json import dumps
from Error import AccessError

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
    
def get_channels(data):
    return data['channels']

def find_uid_in_channel(detail, channel_id, auth_id):
    for ch_id in detail:
        if ch_id['channel_id'] == channel_id:
            for uid in ch_id['user_list']:
                if uid['u_id'] == auth_id:
                    return uid
    return None
     
def find_channel_name(data, channel_id):
    for name in data['channels']:
        if name['channel_id'] == channel_id:
            return name['name']
    return None
    
def find_ownership(user_list):
    owner_member = []
    for owner in user_list:
        if owner[is_owner] == True:
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
def ch_create():
    stack_channel = []
    global Data
    # get the token
    token = request.form.get('token')
    # name the channel
    channel_name = request.form.get('channel_name')
    # set a channel to public or private
    is_public = request.form.get('is_public')
    
    # check is the channel name is valid
    if (len(channel_name) > 20):
        raise ValueError('The maximum characters of name is 20.')
        
    channel_id = Data['counter'].get('channel') + 1
    detail = get_channels(Data)
    # assume channel_data
    channel_data = {
        'name': channel_name,
        'channel_id': channel_id,
        'user_list': [
            {
                'u_id': 456, 
                'name_first': 'test2', 
                'name_last': 'test2', 
                'is_owner': True
            }
        ],
        'is_public': is_public
    }
    detail.append(channel_data)
    
    # return a channel id
    return {
        'channel_id': channel_id
    }

def ch_invite():
    '''
    ValueError when:
    channel_id does not refer to a valid channel that the authorised user is 
    part of.
    u_id does not refer to a valid user
    '''
    
    
    
    # check validation of channel id
    if find_channel(Data, channel_id) == None:
        raise ValueError('Invalid channel')
    # check validation of uid
    valid_user = find_uid(Data, u_id)
    if valid_user == None:
        raise ValueError('Invalid u_id')
    
    # check is the auth user is a member or not of that channel
    user = find_user(Data, token)
    auth_uid = 0
    if user != None:
        auth_uid = user['u_id']
        
    detail = get_channels(Data)
    if find_uid_in_channel(detail, channel_id, auth_uid) == None:
        raise AccessError('Not a member')
    
    # update the data, a new member added
    user_data = {
        'u_id': u_id,
        'name_first': valid_user['name_first'],
        'name_last': valid_user['name_last']
    }
    detail['user_list'].append(user_data)
    return {}

def ch_details():
    stack_channel = []
    global Data
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    detail = get_channels(Data)
    # check validation of channel id
    if find_channel(Data, channel_id) == None:
        raise ValueError('Invalid channel')
    # check auth user is a member or not
    user = find_user(Data, token)
    if user != False:
        auth_id = user['u_id']
    if find_uid_in_channel(detail, channel_id, auth_id) == None:
        raise AccessError('Not a member of that channel')
    
    name = find_channel_name(Data, channel_id)
    channel = find_channel(Data, channel_id)
    owner = find_ownership(channel['user_list'])
    
    
    stack_channel.append(name)
    stack_channel.append(owner)
    stack_channel.append(channel['user_list'])
    return {stack_channel}

'''
def ch_message():
    return dumps({})
'''

def ch_leave():
    global Data
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
    global Data
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
    global Data
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
    global Data
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
    global Data
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
    global Data
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
    

