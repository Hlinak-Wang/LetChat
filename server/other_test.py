import objectToTest as ot
import pytest

# This function is to create a valid account
# and a public channel 
# which would be used in other test_function
def account_And_channel():
    token = ot.auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    channel_id = ot.channels_create(token, 'hhhaaa', True)
    return token, channel_id

def test_standup_start():

    token, channel_id = account_And_channel()
    channel_not_exist = channel_id - 199

    with pytest.raises(ValueError):

        # Channel does not exist
        ot.standup_start(token, channel_not_exist)

    with pytest.raises(AccessError):
        
        # The authorised user is not a member of the channel that message is within


def test_standup_send():


    with pytest.raises(ValueError):


    with pytest.raises(AccessError):


def test_search():

    pass

def test_userpermission_change():


    with pytest.raises(ValueError):

        # U_id doesn't refer to a valid user

        # Permission_id doesn't refer to a value permission

    with pytest.raises(AccessError):

        # The authorised user is not an admin or owner