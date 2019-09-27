def test_sendlater():

    token = 'abc'
    channel_id = 3456
    message = ""
    #message more than 1000 charater
    for i in range(0,1010):
        message += "a"
    
    assert message_sendlater(token, channel_id, message, time_send) == "Message more than 1000 characters"


    


def test_send():

    #message more than 1000 charater
    for i in range(0,1010):
        message += "a"

    assert message_send(token, channel_id, message) == "Message more than 1000 characters"

def test_remove():


    pass

def test_edit():

    pass
    
def test_react():

    pass

def test_unreact():

    pass

def test_pin():

    pass

def test_unpin():


    pass
