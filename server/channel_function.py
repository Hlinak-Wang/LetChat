from flask import Flask, request
from json import dumps
from Error import AccessError

APP = Flask(__name__)

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
    


data = {
    "user_data": {
        234: {
            "mail": "23@23.com",
            "name_first": "ads", 
            "name_last": "fkk", 
            "token": "123", 
            "photo": "nal.img", 
            "handle": "adsfkk",
        },
    },
    "channel": {
        "channel_id": {
            "name": "aed", 
            "all_member": [{
                "u_id": 234,
                "name_first": "ads", 
                "name_last": "fkk",
            }], 
            "owner_member": [{
                "u_id": 234, 
                "name_first": "ads", 
                "name_last": "fkk",
            }],
        },
    },
    "message": {
        "message_id": {
            "u_id": 677, 
            "content": "hey", 
            "time_send": "datetime", 
            "is_unread": True, 
            "is_pinned": True, 
            "is_react":[{"react_id": 1, "u_ids": 2}]
        },
    },
}
def getData():
    global data
    return data.get('channel')
stack_channel = []

# create a channel
def ch_create():
    global stack_channel
    token = request.form.get('token')
    # name the channel
    channel_name = request.form.get('channel_name')
    # check is the channel name is valid
    if (len(channel_name) > 20):
        raise ValueError("The maximum characters of name is 20.")
    # set a channel to public or private
    is_public = request.form.get('is_public')
    channel = Channel(channel_name, is_public, 123, 145)
    channel = channel.__dict__
    stack_channel.append(channel)
    # stack_channel here is a channel_id
    data = getData()
    data[stack_channel] = {
        'name': channel_name,
        'all_member': [{
            'u_id': 123,
            'name_first': 'asd',       # -----> name first
            'name_last': 'zxc',        # -----> name last
        }],
    }
    
    # return a channel id
    return dumps(stack_channel)

def ch_invite():
    '''
    ValueError when:
    channel_id does not refer to a valid channel that the authorised user is 
    part of.
    u_id does not refer to a valid user
    '''
    detail = getData()
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    
    # assume validation of channel
    valid_ch = 'hhh123'
    if channel_id != valid_ch:
        raise ValueError("Invalid channel")
        
    # assume validation of a user id
    valid_uid = 123
    #if uid in not in detail[channel_id]['all_member']:
    if u_id != valid_uid:
        raise ValueError("Invalid u_id")
    
    
    # assume an authorised uid
    auth_uid = 456
    count = 0
    for uid in data[channel_id]['all_member'][i].get('uid'):
        if uid == auth_uid:
            count = 1
        i = i + 1
    if count != 1:
        raise AccessError("Not a member of the channel")
    
    # assume user_information
    user_detail = {
        'u_id': u_id,
        'name_first': 'abc',
        'name_last': 'xyz',
    }

    # update the data, a new member
    detail[channel_id]['all_member'].append(user_detail)
    return dumps({})

def ch_details():
    global stack_channel
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    data = getData()
    count = 0
    for channelid in data[i]:
        if channel_id == channelid:
            count = 1
        i = i + 1
    if count == 0:
        raise ValueError("Invalid channel")
    # assume auth_uid
    auth_uid = 123
    count = 0
    if auth_uid == data[channel_id]['all_member'].get('u_id'):
        count = 1
        
    if count != 1:
        raise AccessError("Not a member of that channel")
    
    stack_channel.append(data[self.get_name()])
    stack_channel.append(data['owner_member'])
    stack_channel.append(data['all_member'])
    return dumps({stack_channel})

'''
def ch_message():
    return dumps({})
'''

def ch_leave():
    data = getData()
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    # check validation of ch_id
    count = 0
    for channelid in data[i]:
        if channel_id == channelid:
            count = 1
        i = i + 1
    
    if count == 0:   # or use token to check
        raise ValueError("Channel ID is invalid")
    u_id = self.get_u_id()
    # assume user_data
    user_data = {
        'u_id': u_id,
        'name_first': 'abc',
        'name_last': 'xyz',
    }
    # remove a list of that user's data
    data[channel_id]['all_member'].remove(user_data)
    return dumps({})

def ch_join():
    data = getData()
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    # check validation of ch_id
    count = 0
    for channelid in data[i]:
        if channel_id == channelid:
            count = 1
        i = i + 1
    if count == 0:
        raise ValueError("Channel ID is invalid")
    # check the channel is public or private
    # assume the admin has u_id 1
    if self.get_state_of_channel() == False and self.get_u_id != 1:
        raise AccessError("The channel is private")
    u_id = self.get_u_id()
    
    # assume user_data
    user_data = {
        'u_id': u_id,
        'name_first': 'abc',
        'name_last': 'xyz',
    }
    # add a list of that user's data
    data[channel_id]['all_member'].append(user_data)
    return dumps({})
    
def ch_addowner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    data = getData()
    # accesserror when the auth_user is not an owner of the slackr or channel
    # Write something here...
    
    # check validation of the channel id
    count = 0
    for channelid in data[i]:
        if channel_id == channelid:
            count = 1
        i = i + 1
    if count == 0:
        raise ValueError("Invalid Channel ID")
    
    # check the user is already the owner or not
    i = 0
    for uid in data[channel_id]['owner_member'][i]:
        if u_id == uid.get('u_id'):
            raise ValueError("Already an owner of that channel")
        i = i + 1 
    # assume user_data
    user_data = {
        'u_id': u_id,
        'name_first': 'abc',
        'name_last': 'xyz',
    }
    data[channel_id]['owner_member'].append(user_data)
    return dumps({})
    
def ch_removeowner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    data = getData()
    # accesserror when the auth_user is not an owner of the slackr or channel
    # Write something here...
    
    # check validation of teh channel id
    count = 0
    for channelid in data[i]:
        if channel_id == channelid:
            count = 1
        i = i + 1
    if count == 0:
        raise ValueError("Invalid Channel ID")
        
    # check the user is owner or not
    for uid in data[channel_id]['owner_member'][i]:
        if u_id == uid.get('u_id'):
            count = 2;
    if count == 1:
        raise ValueError("Not an owner")
    user_data = {
        'u_id': u_id,
        'name_first': 'abc',
        'name_last': 'xyz',
    }
    data[channel_id]['owner_member'].remove(user_data)
    return dumps({})
    
def ch_lists():
    data = getData()
    token = request.args.get('token')
    global stack_channel
    # check the token is valid or not
    # go through lists, if the user is part of channel,
    # using stack_channel to append
    # Provide a list of all channels the the user is part of
    
    # assume the user is part of this channel
    channel1_data = {
        'ch1_id': {
            'name': 'qwe',
            'all_member': [{
                'u_id': 123,
                'name_first': 'abc',
                'name_last': 'xyz',
            }],
            'owner_member': [{
                'u_id': 123,
                'name_first': 'abc',
                'name_last': 'xyz',
            }]
        }
    }

    stack_channel.append(channel1_data)
    return dumps({stack_channel})
    
def ch_listall():
    data = getData()
    token = request.args.get('token')
    # if token is valid
    # a list of all channels will be provided
    
    # assume these are the all channels
    channel1_data = {
        'ch1_id': {
            'name': 'qwe',
            'all_member': [{
                'u_id': 123,
                'name_first': 'abc',
                'name_last': 'xyz',
            }],
            'owner_member': [{
                'u_id': 123,
                'name_first': 'abc',
                'name_last': 'xyz',
            }]
        }
    }
    channel2_data = {
        'ch2_id': {
            'name': 'asd',
            'all_member': [{
                'u_id': 456,
                'name_first': 'qaz',
                'name_last': 'plm',
            }],
            'owner_member': [{
                'u_id': 456,
                'name_first': 'qaz',
                'name_last': 'plm',
            }]
        }
    }
    stack_channel.append(channel1_data)
    stack_channel.append(channel2_data)
    return dumps({data})
    

