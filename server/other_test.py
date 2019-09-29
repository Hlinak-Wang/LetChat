import pytest
import datetime

def auth_register(email, password, first_nanme, last_name):
	
	u_id = 123
	token = 355
	return u_id, token

def channels_create(token, name, is_public):
	channel_id = 12345
	return channel_id

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

def message_send(token, channel_id, message):
    pass

# This function is to create a valid account
# and a public channel 
# which would be used in other test_function

def test_standup_start():
    
    # Create a user and channel, then join the user into the channel
    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    channel_id = channels_create(token, 'hhhaaa', True)
    channel_join(token, channel_id)
    
    # Create a user but no in the channel
    token_not_inchannel, u_id_not_inchannel = auth_register('112342546@gmail.com', 123412, 'TTT', 'LQQQ')
    
    channel_not_exist = channel_id - 199
    
    # Invalid input
    with pytest.raises(ValueError, match=r".*Channeldoes not exist.*"):

        standup_start(token, channel_not_exist)
        
    with pytest.raises(Exception, match=r".*The authorised user is not a member .*"):
        
        standup_start(token_not_inchannel, channel_id)

    # Valid input
    time_now = datetime.datetime.now()
    time_15min_later = datetime(time_now.year, time_now.month, time_now.hour, time_now.minute + 15)
    time_finish = standup_start(token, channel_id)
    assert time_finish == time_15min_later

def test_standup_send():

    # Create a user and channel, then join the user into the channel
    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    channel_id = channels_create(token, 'hhhaaa', True)
    channel_join(token, channel_id)
    
    # Create a user but no in the channel
    token_not_inchannel, u_id_not_inchannel = auth_register('112342546@gmail.com', 123412, 'TTT', 'LQQQ')
    channel_not_valid = channel_id - 100
    
    message_short = 'testing'
    message_long = ''
    for i in range(0,1010):
        message_long += '1'
    
    # Test in the environment of standup has started
    time_finish = standup_start(token, channel_id)
    with pytest.raises(ValueError, match=r".*Channel does not exist.*"):

        standup_send(token, channel_not_valid, message_short)

    with pytest.raises(ValueError, match=r".*Message is more than 1000 characters.*"):

        standup_send(token, channel_id, message_long)

    with pytest.raises(Exception, match=r".*The authorised user is not a member of the channel .*"):
        standup_send(token_not_inchannel, channel_id, message_short)
    
    with pytest.raises(Exception, match=r".*If the standup time has stopped.*"):
        standup_send(token, channel_id, message_short)

def test_search():

    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    channel_id = channels_create(token, 'hhhaaa', True)
    
    # No message
    assert search(token, "No message was sent") == [{}]
    
    # One message
    message_1 = "First message"
    time_now = datetime.datetime.now()
    message_send(token, channel_id, message_1)

    assert search(token, "First_message") == [{"message_id" : 0, "u_id" : u_id, "message" : message_1, "time_create" : time_now, "is_unread" : True}]
    
    # Two message
    message_2 = "Second message"
    time_now2 = datetime.datetime.now()
    message_send(token, channel_id, message_2)
    
    assert search(token, "First_message") == [{"message_id" : 0, "u_id" : u_id, "message" : message_1, "time_create" : time_now, "is_unread" : True},
                                              {"message_id" : 1, "u_id" : u_id, "message" : message_2, "time_create" : time_now2, "is_unread" : True}]

def test_userpermission_change():

    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    u_id_not_valid = u_id - 100000
    
    
    with pytest.raises(ValueError, match=r".*u_id does not refer to a valid user.*"):

        # U_id doesn't refer to a valid user
        admin_userpermission_change(token, u_id_not_valid, permission_id)

    with pytest.raises(ValueError, match=r".*permission_id does not refer to a value permission.*"):
        # Permission_id doesn't refer to a value permission
        admin_userpermission_change(token, u_id, permission_id)

    with pytest.raises(Exception, match=r".*The authorised user is not an admin or owner.*"):

        # The authorised user is not an admin or owner
        admin_userpermission_change(token, u_id, permission_id)