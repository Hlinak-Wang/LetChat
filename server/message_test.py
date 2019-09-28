import objectToTest as ot
import datetime

# This function is to create a valid account
# and a public channel 
# which would be used in other test_function
def account_ANd_channel():
    token = ot.auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    channel_id = ot.channels_create(token, 'hhhaaa', True)
    return token, channel_id

def test_sendlater():

    # Create valid token and channel for testing
    token, channel_id = account_ANd_channel()

    #message more than 1000 charater
    message = ""
    for i in range(0,1010):
        message += "a"
    time_send = datetime.datetime.now()
    assert ot.message_sendlater(token, channel_id, message, time_send) == "Message more than 1000 characters"

    #Time send is a time in the pass
    message = 'send message to the past'
    time_past = datetime(time_send.year - 1, time_send.month, time_send.hour, time_send.minute)
    assert ot.message_sendlater(token, channel_id, message, time_past) == "Time sent is a time in the past"

    #send message to channel doesn't exist
    channel_id = channel_id - 100
    message = 'channel not exist~~~~'
    time_send = datetime.datetime.now()
    assert ot.message_sendlater(token, channel_id, message, time_send) == "Channel doesn't exist"


def test_send():
    # Create valid token and channel for testing
    token, channel_id = account_ANd_channel()

    # Message more than 1000 charater
    message = ""
    for i in range(0,1010):
        message += "a"
    assert ot.message_send(token, channel_id, message) == "Message more than 1000 characters"

def test_remove():
    
    # Create valid token and channel for testing
    token, channel_id = account_ANd_channel()

    #user have no permission to remove the row
    token = 'nopermission'
    message_id = 3451
    assert ot.message_remove(token, message_id) == 'User does not have permission to remove that row'
    
    
    #message not exist
    message_id = 2342
    assert ot.message_remove(token, message_id) == 'Message no longer exists'




def test_edit():

    token, channel_id = account_ANd_channel()

    #invalid message: sent by authorised user
    message_id = '123'
    message = 'asdfagda'
    assert ot.message_edit(token, message_id, message) == 'message_id not valid'


    
def test_react():

    pass

def test_unreact():

    pass

def test_pin():

    pass

def test_unpin():


    pass
