from Error import AccessError

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

def test_channel_invite_ok():
    {u_id, token } = auth_login("123456@gmail.com", "123456789")
    {u_id1, token1 } = auth_login("123456789@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)

    channel_invite(token, channel_id, u_id1)


def test_channel_invite_bad():
 
    {u_id, token } = auth_login("123456@gmail.com", "123456789")
    {u_id1, token1 } = auth_login("123456789@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    with pytest.raises(Exception, match=r"*Channel (based on ID) does not exist*"):
        channel_invite(token, "2222", u_id1)

    with pytest.raises(Exception, match=r"*User is not part of Channel*"):
        channel_invite(token1, channel_id, u_id)

    with pytest.raises(Exception, match=r"*u_id does not refer to a valid user*"):
        channel_invite(token, channel_id, "55555")


def test_channel_details_ok():

    {u_id, token } = auth_login("123456@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)

    channel_details(token, channel_id)


def test_channel_details_bad():
    {u_id, token } = auth_login("123456@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)

    #ValueError
    with pytest.raises(Exception, match=r"*Channel (based on ID) does not exist*"):
        channel_details(token, "123456")

    #AccessError 
    with pytest.raises(Exception, match=r"*User is not a member of Channel*"):
        channel_details("123456", channel_id)


def test_channel_messages_ok():

    {u_id, token } = auth_login("123456@gmail.com", "123456789")
    {u_id1, token1 } = auth_login("123456789@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)

    channel_messages(token, channel_id, 0) = {messages, start, end}
    assert end = start + 50 or -1


def test_channel_messages_bad():
    {u_id, token } = auth_login("123456@gmail.com", "123456789")
    {u_id1, token1 } = auth_login("123456789@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    with pytest.raises(Exception, match=r"*Channel (based on ID) does not exis*"):
        channel_messages(token, channel_id, 0)

    with pytest.raises(Exception, match=r"*start is greater than the total number of messages in the channel*"):
        channel_messages(token, channel_id, 999999999)

    #AccessError 
    with pytest.raises(Exception, match=r"*User is not a member of Channel*"):
        channel_messages(token1, channel_id, 0)




def test_channel_leave_ok():

    channel_id = channels_create("token", "12345", is_public)

    channel_leave("token", channel_id)

def test_channel_leave_bad():
    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    with pytest.raises(Exception, match=r"*Channel (based on ID) does not exist*"):
        channel_leave("token", 11111)


def test_channel_join_ok():

    channel_id = channels_create("token", "12345", is_public)

    channel_join("token", channel_id)


def test_channel_join_bad():
    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    with pytest.raises(Exception, match=r"*Channel (based on ID) does not exist*"):
        channel_join("token", 11111)


    #AccessError
    channel_id = channels_create("token", "12345", is_private)
    with pytest.raises(Exception, match=r"*channel is private*"):
        channel_join("token1", channel_id)



def test_channel_addowner_ok():

    {u_id, token } = auth_login("123456@gmail.com", "123456789")
    {u_id1, token1 } = auth_login("123456789@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)

    channel_addowner(token, channel_id, token1)


def test_channel_addowner_bad():
    {u_id, token } = auth_login("123456@gmail.com", "123456789")
    {u_id1, token1 } = auth_login("123456789@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    with pytest.raises(Exception, match=r"*Channel (based on ID) does not exist*"):
    channel_addowner(token, "2222", u_id1)

    with pytest.raises(Exception, match=r"*User already an owner of the channel*"):
    channel_addowner(token, channel_id, u_id)

    #AccessError 
    with pytest.raises(Exception, match=r"*user is not an owner of the slackr, or an owner of this channel*"):
    channel_addowner(token1, channel_id, u_id)


def test_channel_removeowner_ok():
    {u_id, token } = auth_login("123456@gmail.com", "123456789")
    {u_id1, token1 } = auth_login("123456789@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)

    channel_removeowner(token, channel_id, token1)



def test_channel_removeowner()_bad:
    {u_id, token } = auth_login("123456@gmail.com", "123456789")
    {u_id1, token1 } = auth_login("123456789@gmail.com", "123456789")

    channel_id = channels_create("token", "12345", is_public)
    #ValueError
    with pytest.raises(Exception, match=r"*Channel (based on ID) does not exist*"):
        channel_removeowner(token, "2222", token1)

    with pytest.raises(Exception, match=r"*User is not an owner of the channel*"):
        channel_removeowner(token, channel_id, token1)

    #AccessError 
    with pytest.raises(Exception, match=r"*user is not an owner of the slackr, or an owner of this channel*"):
    channel_addowner(token1, channel_id, token)


def test_channels_list():
    assert channels_list(token) = channels

def test_channels_listall():
    assert channels_listall(token) = channels


def test_channels_create_ok():

    assert type(channels_create("token", "012345", is_public)) = int


def test_channels_create_bad():
    #ValueError
    with pytest.raises(Exception, match=r"*Name too long*"):
        channels_create("token", "012345678901234567890123456789", is_public)
