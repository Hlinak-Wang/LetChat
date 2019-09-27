import objectToTest as ot

def test_sendlater():

    token = 'abc'
    channel_id = 3456
    message = ""
    #message more than 1000 charater
    for i in range(0,1010):
        message += "a"
    
    assert ot.message_sendlater(token, channel_id, message, time_send) == "Message more than 1000 characters"

def test_send():

    #message more than 1000 charater
    for i in range(0,1010):
        message += "a"

    assert ot.message_send(token, channel_id, message) == "Message more than 1000 characters"

def test_remove():
    
    #message not exist
    token = 'asdf'
    message_id = 2342
    assert ot.message_remove(token, message_id) == 'Message no longer exists'

    #user have no permission to remove the row
    token = 'nopermission'
    message_id = 3451
    assert ot.message_remove(token, message_id) == 'User does not have permission to remove that row'

 

    pass

def test_edit():

    token = 'asedf'

    #invalid message: sent by authorised user
    message_id = '123'
    message = 'asdfagda'
    assert ot.message_edit(token, message_id, message) == 'message_id not valid'


    pass
    
def test_react():

    pass

def test_unreact():

    pass

def test_pin():

    pass

def test_unpin():


    pass
