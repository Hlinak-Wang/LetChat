import datetime
import pytest

def auth_register(email, password, first_nanme, last_name):

    pass

def channels_create(token, name, is_public):

    pass

def channel_join(token, channel_id):
    pass

def channel_messages(token, channel_id, start):
    pass

def message_sendlater(token, channel_id, message, time_sent):
	pass

def message_send(token, channel_id, message):
	pass

def message_remove(token, message_id):
	pass

def message_edit(token, message_id, message):
	pass

def message_react(token, message_id, react_id):
	pass

def message_unreact(token, message_id, react_id):
	pass

def message_pin(token, message_id):
	pass

def message_unpin(token, message_id):
	pass
def userpermission_change(token, u_id, permission_id):
    pass

# This function is to create a valid account
# and a public channel 
# which would be used in other test_function
def create_join_send():
    
    # Create valid token and channel for testing
    auth_key = auth_register('123@gmail.com', '12345', 'Hello', 'bye')
    channel = channels_create(auth_key["token"], 'hello', True)
    
    # Assume the user join the channel before send the message
    channel_join(auth_key["token"], channel["id"])
    message_send(auth_key["token"], channel["id"], 'presend message')
    
    return_value = channel_messages(auth_key["token"],channel["id"], 0)
    message_list = return_value["messages"]
    
    return (auth_key, channel, message_list)

def test_sendlater():
    
    # basic setup for testing
    (auth_key, channel, message_list) = create_join_send()
    channel_notexist = channel["id"] - 100
    
    message_long = ""
    for i in range(0,1010):
        message_long += "a"

    message_short = "hello~~"

    time_now = datetime.datetime.now()
    time_past = datetime(time_now.year - 1, time_now.month, time_now.hour, time_now.minute)
    
	# Testing invalid input
    with pytest.raises(ValueError, match=r".* Channel does not exist *."):
        message_sendlater(auth_key["token"], channel_notexist, message_short, time_now)
    
    with pytest.raises(ValueError, match=r".* Message is more than 1000 *."):
        message_sendlater(auth_key["token"], channel["id"], message_long, time_now)
        
    with pytest.raises(ValueError, match=r".* Time sent is a time in the past *."):
        message_sendlater(auth_key["token"], channel["id"], message_short, time_past)
        
    # testing Valid input
    message_sendlater(auth_key["token"], channel["id"], message_short, time_now)
    return_value = channel_messages(auth_key["token"],channel["id"], 0)
    message_list = return_value["messages"]
    
    assert message_list[0]["message"] == message_short

def test_send():
    
    # basic setup for testing
    (auth_key, channel, message_list) = create_join_send()
    
    message_long = ""
    for i in range(0,1010):
        message_long += "a"
    
    message_short = 'testing'
    # Invalid input
    with pytest.raises(ValueError, match=r".* Message is more than 1000 characters *."):

        message_send(auth_key["token"], channel["id"], message_long)
        
    # Valid input
    message_send(auth_key["token"], channel["id"], message_short)
    return_value = channel_messages(auth_key["token"],channel["id"], 0)
    message_list = return_value["messages"]
    assert message_list[0]["message"] == message_short
    
def test_remove():
    
    # Create an admin
    auth_key_admin = auth_register('asdf@gmail.com','asdfagf','adsffgdhf','sdfdgfhg')
    
    # basic setup for testing assuming this user is owner of channel
    (auth_key_owner, channel, message_list) = create_join_send()
    
    # let the admin to join the channel
    channel_join(auth_key_admin["token"], channel["id"])
    message_send(auth_key_admin["token"], channel["id"], "admin's message")
    # Create other user again
    auth_key = auth_register('asdf@gmail.com','asdfagf','adsffgdhf','sdfdgfhg')
    channel_join(auth_key["token"], channel["id"])
    message_send(auth_key["token"], channel["id"], "normal user's message")
    message_send(auth_key["token"], channel["id"], "normal user's message 2")
    
    # Obtain the message list
    return_value = channel_messages(auth_key_owner["token"],channel["id"], 0)
    message_list = return_value["messages"]
    
    # Invalid input 
    # All requirement fail
    with pytest.raises(Exception,match=r".*AccessError.*"):
        message_remove(auth_key["token"], message_list[1]["message_id"])
    
    # One of the reequirement sucess
    # Message with message_id was sent by the authorised user making this request
    message_remove(auth_key["token"], message_list[0]["message_id"])
    
    # Message with message_id was sent by an owner of this channel 
    message_remove(auth_key_owner["token"], message_list[1]["message_id"])
    
    # Message with message_id was sent by an admin or owner of the slack
    message_remove(auth_key_admin["token"], message_list[3]["message_id"])
    
    # If the message removed above is successful, the next test should raises exception
    with pytest.raises(ValueError, match=r".* Message no longer exists.*"):
        message_remove(auth_key["token"], message_list[0]["message_id"])
        message_remove(auth_key_admin["token"], message_list[1]["message_id"])
        message_remove(auth_key_owner["token"], message_list[3]["message_id"])
        
def test_edit():
    
    # Create an admin
    auth_key_admin = auth_register('asdf@gmail.com','asdfagf','adsffgdhf','sdfdgfhg') 
    # basic setup for testing assuming this user is channel owner
    (auth_key_owner, channel, message_list) = create_join_send()
    
    # let the admin to join the channel
    channel_join(auth_key_admin["token"], channel["id"])
    message_send(auth_key_admin["token"], channel["id"], "admin's message")
    
    # Create normal user and join the channel
    auth_key = auth_register('assadfghjdzfdf@gmail.com','asdfagf','adsffgdhf','sdfdgfhg') 
    channel_join(auth_key_admin["token"], channel["id"])
    message_send(auth_key_admin["token"], channel["id"], "normal user's message")
    
    # Obtain message list
    return_value = channel_messages(auth_key_owner["token"],channel["id"], 0)
    message_list = return_value["messages"]
    # Invalid input
    # All reequirement fail (normal user try to edit other's message)
    with pytest.raises(ValueError, match=r".*AccessError*."):
        message_edit(auth_key["token"], message_list[1]["message_id"], "new_message")

def test_react():

    # basic setup for testing
    (auth_key, channel, message_list) = create_join_send()

    message_notValid = message_list[0]["message_id"] + 1000
    react_valid = 12
    react_notvalid = 1232130000
    
    # Invalid input
    with pytest.raises(ValueError, match=r".*message_id is not a valid message *."):
        message_react(auth_key["token"], message_notValid, react_valid)
    
    with pytest.raises(ValueError, match=r".*react_id is not a valid React ID*."):
        message_react(auth_key["token"], message_list[0]["message_id"], react_notvalid)
    
    # React the message in advance
    # If the next text raises an exception means the react is successfully added
    message_react(auth_key["token"], message_list[0]["message_id"], react_valid)

    # React the message again see whether raise exception
    with pytest.raises(ValueError, match=r".* message_id already contains an active React with ID react_id.*"):
        message_react(auth_key["token"], message_list[0]["message_id"], react_valid)

    
def test_unreact():

    # basic setup for testing
    (auth_key, channel, message_list) = create_join_send()

    message_notValid = message_list[0]["message_id"] + 1000
    react_valid = 12
    react_notvalid = 1232130000
    
    # React the message for testing in advance
    message_react(auth_key["token"], message_list[0]["message_id"], react_valid)
    
    # Invalid input
    with pytest.raises(ValueError, match=r".*message_id is not a valid message *."):
        message_unreact(auth_key["token"], message_notValid, react_valid)

    with pytest.raises(ValueError, match=r".*react_id is not a valid React ID*."):
        message_unreact(auth_key["token"], message_list[0]["message_id"], react_notvalid)

    # Remove the react in advance
    # If the next text raises an exception means the react is successfully removed
    message_unreact(auth_key["token"], message_list[0]["message_id"], react_valid)
    
    # Unreact the message again see whether raise excepion
    with pytest.raises(ValueError, match=r".* message_id does not contain an active React with ID react_id.*"):
        message_unreact(auth_key["token"], message_list[0]["message_id"], react_valid)

def test_pin():

    # basic setup for testing
    (auth_key, channel, message_list) = create_join_send()

    # Invalid input
    with pytest.raises(ValueError, match=r".*message_id is not a valid message.*"):
        message_pin(auth_key["token"], message_list[0]["message_id"] + 100000000)

    with pytest.raises(ValueError, match=r"The authorised user is not an admin.*"):
        # Assuming the default permission_id for all user is 3
        message_pin(auth_key["token"], message_list[0]["message_id"])   
    
    # Create other user for testing
    auth_key2 = auth_register('1234567@gmail.com', "asdfa","asdf")
    with pytest.raises(Exception, match=r".*The authorised user is not a member of the channel that the message is within.*"):
        message_pin(auth_key2["token"], message_list[0]["message_id"])
    
    userpermission_change(auth_key["token"], auth_key["token"], 2)
    # Pin the message in advance, if the next test raise exception
    # means the message is successfully pinned
    message_pin(auth_key["token"], message_list[0]["message_id"])
    
    with pytest.raises(ValueError, match=r".*Message with ID message_id is already pinned.*"):
        message_pin(auth_key["token"], message_list[0]["message_id"])

def test_unpin():

    # basic setup for testing
    (auth_key, channel, message_list) = create_join_send()
    
    # Change the user's permission_id to 2(Admin)
    userpermission_change(auth_key["token"], auth_key["token"], 2)
    
    # Create other user for testing
    auth_key2 = create_join_send()
    
    # Create other user but not in channel for testing
    auth_key3 = auth_register('1234567@gmail.com', "asdfa","asdf")
    
    # Pin the message in advance for testing
    message_pin(auth_key["token"], message_list[0]["message_id"])
    
    # Invalid input
    with pytest.raises(ValueError, match=r".*message_id is not a valid message.*"):
        
        message_unpin(auth_key["token"], message_list[0]["message_id"] + 100000000)

    with pytest.raises(ValueError, match=r".*The authorised user is not an admin.*"):

        # Assuming the default permission_id for all user is 3
        message_unpin(auth_key2["token"], message_list[0]["message_id"])   

    with pytest.raises(Exception, match=r".*The authorised user is not a member of the channel that the message is within.*"):
        message_unpin(auth_key3["token"], message_list[0]["message_id"])
    
    # Pin the message in advance, if the next test raise exception
    # means the message is successfully pinned
    message_unpin(auth_key["token"], message_list[0]["message_id"])
    
    with pytest.raises(ValueError, match=r".*Message with ID message_id is already pinned.*"):
        message_unpin(auth_key["token"], message_list[0]["message_id"])
