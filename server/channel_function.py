from flask import Flask, request
from json import dumps

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
    if uid in not in detail:    # uid need to change
        raise Exception(f"Access Error -> Not a authorised user")
    
    # update the data, a new member

    return dumps({})

def ch_details():
    global stack_channel
    # AccessError whenAuthorised user is not a 
    # member of channel with channel_id
    channel_id = request.form.get('channel_id')
    channelinformation = getData()
    if channel_id is in channelinformation:
        stack_channel.append(channelinformation['name'])
        stack_channel.append(channelinformation['owner_member'])
        stack_channel.append(channelinformation['all_member'])
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
    # return a channel id
    return dumps(stack_channel)

def ch_message():
    return dumps({})

def ch_leave():

def ch_join():

def ch_addowner():

def ch_removeowner():

def ch_lists():

def ch_listall():

if __name__ == '__main__':
    APP.run(debug = True)
