def channel_invite(token, channel_id, u_id):
    return 

def channel_details(token, channel_id):
    return name, owner_members, all_members 

def channel_messages(token, channel_id, start):
    return messages, start, end 

def channel_leave(token, channel_id):
    return 

def channel_join(token, channel_id):
    return token 

def channel_addowner(token, channel_id, u_id)):
    return 

def channel_removeowner(token, channel_id, u_id):
    return token 

def channels_list(token):
    return channels  

def channels_listall(token)):
    return channels 

def channels_create(token, name, is_public):
    return channel_id  


import channel_invite
import channel_details
import channel_messages
import channel_leave
import channel_join
import channel_addowner
import channel_removeowner
import channels_list
import channels_listall
import channels_create


def test_channel_invite():
 
    auth_login("123456@gmail.com", "123456789") = token
    auth_login("123456789@gmail.com", "123456789") = token1

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    assert channel_invite(token, "2222", token1) = "Channel (based on ID) does not exist"

    assert channel_invite(token1, channel_id, token) = "User is not part of Channel"

    assert channel_invite(token, channel_id, "55555") = "u_id does not refer to a valid user"

    channel_invite(token, channel_id, token1) = "u_id does not refer to a valid user"


def test_channel_details():
    auth_login("123456@gmail.com", "123456789") = token

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    assert channel_details(token, "123456") = "Channel (based on ID) does not exist"

    #AccessError 
    assert channel_details("123456", channel_id) = "User is not a member of Channel"

    channel_details(token, channel_id)


def test_channel_messages():
    auth_login("123456@gmail.com", "123456789") = token
    auth_login("123456789@gmail.com", "123456789") = token1

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    assert channel_messages(token, channel_id, 0) = "Channel (based on ID) does not exist"

    assert channel_messages(token, channel_id, 999999999) = "start is greater than the total number of messages in the channel"

    #AccessError 
    assert channel_messages(token1, channel_id, 0) = "User is not a member of Channel"

    assert type(channel_messages(token, channel_id, 0)) = int

    assert channel_messages(token, channel_id, 0) = 50 or -1

def test_channel_leave():
    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    assert channel_leave("token", 11111) = "Channel (based on ID) does not exist"

    channel_leave("token", channel_id)


def test_channel_join():
    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    assert channel_join("token", 11111) = "Channel (based on ID) does not exist"


    channel_id = channels_create("token", "12345", is_private)
    #AccessError 
    assert channel_join("token1", channel_id) =  "channel is private"

    channel_id = channels_create("token", "12345", is_public)

    channel_join("token", channel_id)




def test_channel_addowner():
    auth_login("123456@gmail.com", "123456789") = token
    auth_login("123456789@gmail.com", "123456789") = token1

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    assert channel_addowner(token, "2222", token1) = "Channel (based on ID) does not exist"

    assert channel_addowner(token, channel_id, token) = "User already an owner of the channel"

    #AccessError 
    assert channel_addowner(token1, channel_id, token) = "user is not an owner of the slackr, or an owner of this channel"

    channel_addowner(token, channel_id, token1)



def test_channel_removeowner():
    auth_login("123456@gmail.com", "123456789") = token
    auth_login("123456789@gmail.com", "123456789") = token1

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    assert channel_removeowner(token, "2222", token1) = "Channel (based on ID) does not exist"

    assert channel_removeowner(token, channel_id, token1) = "User is not an owner of the channel"

    #AccessError 
    assert channel_addowner(token1, channel_id, token) = "user is not an owner of the slackr, or an owner of this channel"

    channel_addowner(token, channel_id, token1)


def test_channels_list():
    assert channels_list(token) = channels

def test_channels_listall():
    assert channels_listall(token) = channels

def test_channels_create():
    #ValueError
    assert channels_create("token", "012345678901234567890123456789", is_public) = "Name too long"

    assert type(channels_create("token", "012345", is_public)) = int
