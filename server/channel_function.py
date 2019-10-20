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
    "user_data": {234: {"mail": "23@23.com", "name_first": "ads", "name_last": "fkk", "token": "123", "photo": "nal.img", "handle": adsfkk}}
    "channel": {channel_id: {"name": "aed", "all_member": [{"u_id": 234, "name_first": "ads", "name_last": "fkk"}], "owner_member": [{"u_id": 234, "name_first": "ads", "name_last": "fkk"}]}}
    "message": {message_id: {"u_id": 677, "content": "hey", "time_send": "datetime", "is_unread": True, "is_pinned": True, "is_react":[{react_id}: 1, "u_ids": 2]}}

def getData():
    global data
    return data.get('channel')
stack_channel = {}


def ch_invite():
    '''
    ValueError when:
    channel_id does not refer to a valid channel that the authorised user is 
    part of.
    u_id does not refer to a valid user
    '''
    # check the channel id is valid
    channel_id = request.form.get('channel_id')
    # valueerror checking here
    # check the u_id is valid
    u_id = request.form.get('u_id')
    detail = getData()
    if uid in not in detail[channel_id]['all_member']:    # uid need to change
        raise AccessError("Access Error -> Not a authorised user")
    
    # update the data, a new member
    detail[channel_id]['all_member'].append(u_id) # name_first and name_last
    return dumps({})

def ch_details():
    global stack_channel
    # channel_id is invalid
    # check it with token
    channel_id = request.args.get('channel_id')
    information = getData()
    if channel_id is not in information:
        raise AccessError("User is not a member of that channel")
    else:
        stack_channel.append(information[self.get_name()])
        stack_channel.append(information['owner_member'])
        stack_channel.append(information['all_member'])
        return dumps({stack_channel})

# create a channel
def ch_create():
    global stack_channel
    # name the channel
    channel_name = request.form.get('channel_name')
    # check is the channel name is valid
    if (len(channel_name) > 20):
        raise ValueError(f"The maximum characters of name is 20.")
    # set a channel to public or private
    is_public = request.form.get('is_public')
    channel = Channel(channel_name, is_public)
    channel = channel.__dict__
    stack_channel.append(channel)
    # stack_channel here is a channel_id
    data = getData()
    data[stack_channel] = {
        'name': channel_name,
        'all_member': [{
            'u_id': self.get_u_id(),
            'name_first': [],       # -----> name first
            'name_last': [],        # -----> name last
        }]
    }
    
    # return a channel id
    return dumps(stack_channel)

'''
def ch_message():
    return dumps({})
'''

def ch_leave():
    data = getData()
    channel_id = request.form.get('channel_id')
    # check validation of ch_id
    if channel_id is not in data:   # or use token to check
        raise ValueError("Channel ID is invalid")
    u_id = self.get_u_id()
    # not sure what is inside the remove()
    data[channel_id]['all_member'].remove(u_id)
    return dumps({})

def ch_join():
    data = getData()
    channel_id = request.form.get('channel_id')
    # check validation of ch_id
    if channel_id is not in data:
        raise ValueError("Channel ID is invalid")
    # check the channel is public or private
    # assume the admin has u_id 1
    if self.get_state_of_channel() == False and self.get_u_id == 1:
        raise AccessError("The channel is private")
    u_id = self.get_u_id()
    # remove a list of that user's data
    data[channel_id]['all_member'].append(u_id)
    return dumps({})
    
def ch_addowner():
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    data = getData()
    # how to get the authrised user id
    # accesserror when not an owner of slackr or teh channel
    if channel_id is not in data:
        raise ValueError("Invalid Channel ID")
    for uid in data[channel_id]['owner_member']:
        if u_id == uid[0]['u_id']:
            raise ValueError("Already an owner of that channel")
    data[channel_id]['owner_member'] = {
        'u_id': u_id,
        name_first: [],
        name_last: [],
    }
    return dumps({})
    
def ch_removeowner():
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    data = getData()
    count = 0
    # how to get the authrised user id
    # accesserror when not an owner of slackr or teh channel
    if channel_id is not in data:
        raise ValueError("Invalid Channel ID")
    for uid in data[channel_id]['owner_member']:
        if u_id == uid[0]['u_id']:
            count = 1;
    if count == 0:
        raise ValueError("Not an owner")
    data[channel_id]['owner_member'].remove(u_id) # <-a string of data
    return dumps({})
    
def ch_lists():
    data = getData()
    token = request.args.get('token')
    global stack_channel
    # check the token is valid or not
    # go through lists, if the user is part of channel,
    # using stack_channel to append
    # Provide a list of all channels the the user is part of
    return dumps({stack_channel})
    
def ch_listall():
    data = getData()
    token = request.args.get('token')
    # if token is valid
    # a list of all channels will be provided
    return dumps({data})
    
if __name__ == '__main__':
    APP.run(debug = True)
