import objectToTest as ot
import datetime
import pytest

# This function is to create a valid account
# and a public channel 
# which would be used in other test_function
def account_And_channel():
    token = ot.auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    channel_id = ot.channels_create(token, 'hhhaaa', True)
    return token, channel_id

def test_sendlater():

    # Create valid token and channel for testing
    token, channel_id = account_And_channel()
    channel_notexist = channel_id - 100

    message_long = ""
    for i in range(0,1010):
        message += "a"

    message_short = "hello~~"

    time_now = datetime.datetime.now()
    time_past = datetime(time_now.year - 1, time_now.month, time_now.hour, time_now.minute)
    
    with pytest.raises(ValueError):

        #message more than 1000 charater
        ot.message_sendlater(token, channel_id, message_long, time_now)

        #send message to the past
        ot.message_sendlater(token, channel_id, message_short, time_past)
        
        #send message to channel not exist
        ot.message_sendlater(token, channel_notexist, message_short, time_now)


def test_send():
    # Create valid token and channel for testing
    token, channel_id = account_And_channel()

    message_long = ""
    for i in range(0,1010):
        message_long += "a"

    with pytest.raises(ValueError):

        #message more than 1000 charater
        ot.message_send(token, channel_id, message_long)


def test_remove():
    
    # Create valid token and channel for testing
    token, channel_id = account_And_channel()

    message_id = 3451
    with pytest.raises(ValueError):

        # Message no longer exists
        ot.message_remove(token, message_id)

    #with pytest.raises(AccessError):
        #user have no permission to remove the row
        #ot.message_remove(token, message_id)


def test_edit():

    token, channel_id = account_And_channel()

    message_id = '123'
    message = 'asdfagda'

    with pytest.raises(ValueError):

        # editer is not the poster of this message
        ot.message_edit(token, message_id, message)

        # Message sent byy authorised user
        ot.message_edit(token, message_id, message)

        # ???

    #invalid message: sent by authorised user
    

def test_react():

    token, channel_id = account_And_channel()

    message_notValid = 00000
    message_valid = 123214123
    react_valid = 92193
    react_notvalid = 0000

    with pytest.raises(ValueError):

        # message_id is not a valid message within a channel
        ot.message_react(token, message_notValid, react_valid)

        # react_id is not valid
        ot.message_react(token, message_valid, react_notvalid)

        # message has already contain an active react
        ot.message_react(token, message_valid, react_notvalid)

def test_unreact():

    token, channel_id = account_And_channel()

    with pytest.raises(ValueError):

        # message_id is not a valid message within a channel
        ot.message_react(token, message_valid, react_notvalid)

        # react_id is not valid
        ot.message_react(token, message_valid, react_notvalid)

        # message doesn't contain any active react
        ot.message_react(token, message_valid, react_notvalid)



def test_pin():

    token, channel_id = account_And_channel()

    with pytest.raises(ValueError):

        # Message is not a valid message
        ot.message_pin(token, message_id)

        # The authorised user is not an admin
        ot.message_pin(token, message_id)   

        # Message is already pinned
        ot.message_pin(token, message_id)

    with pytest.raises(AccessError):

        # the authorised user is not an menber in the channel where message is within
        ot.message_pin(token, message_id)


def test_unpin():

    token, channel_id = account_And_channel()

    with pytest.raises(ValueError):

        # Message is not a valid message
        ot.message_unpin(token, message_id)

        # The authorised user is not an admin
        ot.message_unpin(token, message_id)   

        # Message is already unpinned
        ot.message_unpin(token, message_id)

    with pytest.raises(AccessError):

        # the authorised user is not an menber in the channel where message is within
        ot.message_unpin(token, message_id)
