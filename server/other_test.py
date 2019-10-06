import pytest
import datetime
from Error import AccessError

def auth_register(email, password, first_nanme, last_name):
	
	pass

def channels_create(token, name, is_public):
	pass

def standup_start(token, channel_id):
    pass

def standup_send(token, channel_id, message):
    pass

def search(toekn, query_str):
    message = [{}]
    return message

def admin_userpermission_change(token, u_id, permission_id):
    pass

def channel_join(token, channel_id):
    pass

def channel_leave(token, channel_id):
    pass

def channel_messages(token, channel_id, start):
    
    pass

def message_send(token, channel_id, message):
    pass

def message_pin(token, message_id):
    pass

def message_unpin(token, message_id):
    pass


def create_join_send():
    
    # Create valid token and channel for testing
    auth_key = auth_register('123@gmail.com', '12345', 'Hello', 'bye')
    channel = channels_create(auth_key["token"], 'hello', True)
    
    # Assume the user join the channel before send the message
    message_send(auth_key["token"], channel["id"], 'presend message')
    
    message_channel = channel_messages(auth_key["token"],channel["id"], 0)
    message_list = message_channel["messages"]
    
    return (auth_key, channel, message_list)
# This function is to create a valid account
# and a public channel 
# which would be used in other test_function

def test_standup_start():
    
    # Create an user and channel, and obtain the message list
    (auth_key, channel, message_list) = create_join_send()
    
    channel_not_exist = channel["id"] - 199
    
    # Invalid input
    with pytest.raises(ValueError, match=r".*Channeldoes not exist.*"):

        standup_start(auth_key["token"], channel_not_exist)
    
    # Usesr leave the channel for testing
    channel_leave(auth_key["token"], channel["id"])
    
    with pytest.raises(AccessError, match=r".*The authorised user is not a member .*"):
        
        standup_start(auth_key["token"], channel["id"])

def test_standup_send():

    # Create an user and channel, and obtain the message list
    (auth_key, channel, message_list) = create_join_send()
    
    channel_not_valid = channel["id"] - 100
    
    message_short = 'testing'
    message_long = ''
    for i in range(0,1010):
        message_long += '1'
    
    # Test in the environment of standup has started
    time_finish = standup_start(auth_key["token"], channel["id"])
    
    # Testing invalid input
    with pytest.raises(ValueError, match=r".*Channel does not exist.*"):

        standup_send(auth_key["token"], channel_not_valid, message_short)

    with pytest.raises(ValueError, match=r".*Message is more than 1000 characters.*"):

        standup_send(auth_key["token"], channel["id"], message_long)

    # Create another user join channel 2, but there is no standup
    auth_key_2, channel_2, message_list = create_join_send()
    
    # Use the situation of no standup start yet to simulate the standup is stoped
    with pytest.raises(AccessError, match=r".*If the standup time has stopped.*"):
        standup_send(auth_key_2["token"], channel_2["id"], message_short)

    # Create a user but no in the channel
    auth_key_3 = auth_register('112342546@gmail.com', 123412, 'TTT', 'LQQQ')
    with pytest.raises(AccessError, match=r".*The authorised user is not a member of the channel .*"):
        standup_send(auth_key_3["token"], channel["id"], message_short)
    
def test_search():

    # Create an user and channel, and obtain the message list
    (auth_key, channel, message_list) = create_join_send()
    
    # No message match
    assert search(auth_key['token'], "No message match") == [{}]
    
    # One message match
    message_1 = "First message"
    time_now = datetime.datetime.now()
    message_send(auth_key['token'], channel["id"], message_1)
    return_value = channel_messages(auth_key["token"],channel["id"], 0)
    message_list = return_value["messages"]

    assert search(auth_key['token'], "First_message") == [{"message_id" : message_list[0]["message_id"], "u_id" : auth_key["u_id"], "message" : message_1, "time_create" : time_now, "is_unread" : True}]
    
    # Two message
    message_2 = "First message"
    time_now2 = datetime.datetime.now()
    message_send(auth_key['token'], channel["id"], message_2)
    return_value = channel_messages(auth_key["token"],channel["id"], 0)
    message_list = return_value["messages"]
    
    assert search(auth_key['token'], "First_message") == [{"message_id" : message_list[0]["message_id"], "u_id" : auth_key["u_id"], "message" : message_1, "time_create" : time_now, "is_unread" : True},
                                                          {"message_id" : message_list[1]["message_id"], "u_id" : auth_key["u_id"], "message" : message_2, "time_create" : time_now2, "is_unread" : True}]

def test_userpermission_change():

    # Create an user and channel, and obtain the message list
    (auth_key_admin, channel, message_list) = create_join_send()
    
    # Create normal user and join the channel
    auth_key = auth_register('asdfghfds@gmail.com','23w4te5rgrfedw', 'asfd','asdf')
    channel_join(auth_key["token"], channel["id"])
    
    u_id_not_valid = auth_key_admin["u_id"] - 100000
    
    # Testing for invalid input
    with pytest.raises(ValueError, match=r".*u_id does not refer to a valid user.*"):

        admin_userpermission_change(auth_key_admin['token'], u_id_not_valid, 2)

    with pytest.raises(ValueError, match=r".*permission_id does not refer to a value permission.*"):

        admin_userpermission_change(auth_key_admin['token'], auth_key['u_id'], 123342545)

    with pytest.raises(AccessError, match=r".*The authorised user is not an admin or owner.*"):

        admin_userpermission_change(auth_key['token'], auth_key_admin['u_id'], 2)
        
    # Testing for valid input
    # change the user_2's permission to admin 
    admin_userpermission_change(auth_key_admin['token'], auth_key['u_id'], 2)
    message_pin(auth_key["token"], message_list[0]["message_id"])