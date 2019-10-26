from Error import AccessError
import pytest
from channel_function import (
        ch_create,
        ch_invite,
        ch_details,
        ch_leave,
        ch_join,
        ch_addowner,
        ch_removeowner,
        ch_lists,
        ch_listall
)


# initial state of testing
def getdata():
    data = {
            'users': [
                {'u_id': 123,
                 'name_first': 'test',
                 'name_last': 'test',
                 'token': '12345',
                 'handle_str': 'testtest',
                 'email': 'test@test.com',
                 'password': 'test',
                 'permission_id': 1,
                 'channel_involve': [1]  # channel_id
                 },
                {'u_id': 1234,
                 'name_first': 'test2',
                 'name_last': 'test2',
                 'token': '123456',
                 'handle_str': 'testtest2',
                 'email': 'test2@test2.com',
                 'password': 'test2',
                 'permission_id': 3,
                 'channel_involve': [1]  # channel_id
                 },
                {'u_id': 12345,
                 'name_first': 'not in channel',
                 'name_last': 'test',
                 'token': '1234567',
                 'handle_str': 'not in channel',
                 'email': 'tests2@tests2.com',
                 'password': 'tesst2',
                 'permission_id': 3,
                 'channel_involve': []  # channel_id
                 }
            ],
            'channels': [{
                'name': 'test',
                'channel_id': 1,
                'user_list': [
                    {'u_id': 123, 'name_first': 'test', 'name_last': 'test',
                     'is_owner': True},
                    {'u_id': 1234, 'name_first': 'test2', 'name_last': 'test2',
                     'is_owner': False}
                ],
                'is_public': True,
                'standup_finish': None,         # time_finish
                'messages': [
                    {
                        'message': 'test',
                        'u_id': 123,
                        'reacts': [{'react_id': 1, 'u_ids': []}],
                        'is_pinned': False,
                        'time_created': '10/20/2019, 23:25:33',
                        'message_id': 1,
                        'channel_id': 1
                    },
                    {
                        'message': 'test2',
                        'u_id': 1234,
                        'reacts': [{'react_id': 1, 'u_ids': []}],
                        'is_pinned': False,
                        'time_created': '10/20/2019, 23:24:33',
                        'message_id': 0,
                        'channel_id': 1
                    }
                ]
            }],
            'message_counter': 0
        }
    return data


# Testing valid input for channel_invite
def test_channel_invite_ok():
    data = getdata()
    user = data['users'][0]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user['token'], '12345', True)
    # it takes in data, token, u_id and channel_id
    ch_invite(data, user['token'], '1234', channel['channel_id'])

    # Check the user is successfully added into channel
    # it takes in data, token and channel_id
    channel_profile = ch_details(data, user['token'], channel['channel_id'])
    member_list = channel_profile['all_members']
    assert member_list[0]['u_id'] == user['u_id']
    assert member_list[1]['u_id'] == 1234


# Testing invalid input for channel_invite
def test_channel_invite_bad():
    data = getdata()
    user = data['users'][0]
    user1 = data['users'][1]
    user2 = data['users'][2]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user['token'], '12345', True)
    res1 = ch_invite(data, user['token'], user1['u_id'], '2222')
    assert res1 == {'ValueError': 'Invalid channel id'}

    res2 = ch_invite(data, user['token'], '55555', channel['channel_id'])
    assert res2 == {'ValueError': 'Invalid u_id'}

    res3 = ch_invite(data, '46653', user2['u_id'], channel['channel_id'])
    assert res3 == {'AccessError': 'the authorised user is not already a \
                    member of the channel'}
    ch_invite(data, user['token'], user1['u_id'], channel['channel_id'])
    res4 = ch_invite(data, user['token'], user1['u_id'], channel['channel_id'])
    assert res4 == {'AccessError': 'The invite user is already a member of \
                    the channel'}



# Testing valid input for channel_details
def test_channel_details_ok():
    data = getdata()
    user = data['users'][0]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user['token'], '12345', True)

    channel_profile = ch_details(data, user['token'], channel['channel_id'])
    print(channel['channel_id'])
    # Checking the output of channel detail
    assert channel_profile['name'] == "12345"

    owner_list = channel_profile["owner_members"]
    assert owner_list[0]["u_id"] == user['u_id']

    member_list = channel_profile["all_members"]
    assert member_list[0]["u_id"] == user['u_id']


# Testing invalid input for channel detail
def test_channel_details_bad():
    data = getdata()
    user = data['users'][0]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user['token'], '12345', True)

    with pytest.raises(ValueError, match=r"*Invalid channel id*"):
        ch_details(data, user['token'], '123456')

    with pytest.raises(AccessError, match=r"*User is not a member of \
                                            Channel*"):
        ch_details(data, '123456', channel['channel_id'])


'''
# Testing valid input for channel_message
def test_channel_messages_ok():
    data = getdata()
    user = data['users'][0]
    channel = ch_create(user['token'], '12345', True)
    message_send(auth_key["token"], channel["id"], "testing")

    message_channel = channel_messages(auth_key["token"], channel["id"], 0)

    # Checking the output
    assert message_channel["start"] == 0
    assert message_channel["end"] == 50

    messages = message_channel["message"]
    assert messages[0]["message"] == "testing"
    assert messages[0]["u_id"] == auth_key["u_id"]


# Testing invalid input for channel_message
def test_channel_messages_bad():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh",
                                   "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf",
                             "asdfzcxv")

    channel = channels_create(auth_key["token"], "12345", True)

    with pytest.raises(ValueError, match=r"*Channel (based on ID) does not \
                                           exis*"):
        channel_messages(auth_key["token"], channel["id"] - 123, 0)

    with pytest.raises(ValueError, match=r"*start is greater than the total\
                                          number of messages in the channel*"):
        channel_messages(auth_key["token"], channel["id"], 999999999)

    with pytest.raises(AccessError, match=r"*User is not a member of \
                                             Channel*"):
        channel_messages(auth_key_admin["token"], channel["id"], 0)
'''


# Testing valid input for channel_leave
def test_channel_leave_ok():
    data = getdata()
    user = data['users'][0]
    # it takes in data, token, channel_name and is_public and return channel_id
    channel = ch_create(data, user['token'], '12345', True)

    ch_join(data, user['token'], channel['channel_id'])
    ch_leave(data, user['token'], channel['channel_id'])

    # Check the member in channel
    channel_profile = ch_details(data, user['token'], channel['channel_id'])
    member_list = channel_profile["all_members"]
    assert member_list[0]["u_id"] == user['u_id']


# Testing invalid input for channel_leave
def test_channel_leave_bad():
    data = getdata()
    user = data['users'][0]
    # it takes in data, token, channel_name and is_public and return channel_id
    channel = ch_create(data, user['token'], '12345', True)

    with pytest.raises(ValueError, match=r"*Channel ID is invalid*"):
        ch_leave(data, user['token'], channel['channel_id'])


# Testing valid input for channel_join
def test_channel_join_ok():
    data = getdata()
    user = data['users'][0]
    channel = ch_create(data, user['token'], '12345', True)
    user2 = data['users'][1]
    ch_join(data, user2['token'], channel['channel_id'])
    channel_profile = ch_details(data, user2['token'], channel['channel_id'])

    # Check the new user has join the channel
    member_list = channel_profile["all_members"]
    assert member_list[0]["u_id"] == user['u_id']
    assert member_list[1]["u_id"] == user2['u_id']


# Testing invalid input for channel_join
def test_channel_join_bad():
    data = getdata()
    user = data['users'][0]
    channel = ch_create(data, user['token'], '12345', True)
    user2 = data['users'][1]
    # ValueError
    with pytest.raises(ValueError, match=r"*Channel ID is invalid*"):
        ch_join(data, user2['token'], channel['channel_id'] - 123)

    # AccessError
    channel2 = ch_create(data, user['token'], '12345', True)
    with pytest.raises(AccessError, match=r"*The channel is private*"):
        ch_join(data, user2['token'], channel2['channel_id'])


# Testing valid input for channel_addowner
def test_channel_addowner_ok():
    data = getdata()
    user = data['users'][0]
    channel = ch_create(data, user['token'], '12345', True)
    user2 = data['users'][1]
    ch_join(data, user2['token'], channel['channel_id'])

    ch_addowner(data, user['token'], channel["id"], user2['u_id'])
    channel_profile = ch_details(data, user['token'], channel['channel_id'])
    owner_list = channel_profile["owner_members"]

    # Checking there is two owner in this channel
    assert owner_list[0]["u_id"] == user['u_id']
    assert owner_list[1]["u_id"] == user2['u_id']


# Testing invalid input for channel_addowner
def test_channel_addowner_bad():
    data = getdata()
    user_admin = data['users'][0]
    user1 = data['users'][1]
    user2 = data['users'][2]
    channel = ch_create(data, user_admin['token'], '12345', True)

    ch_join(data, user1['token'], channel['channel_id'])
    ch_join(data, user2['token'], channel['channel_id'])
    # AccessError
    with pytest.raises(AccessError, match=r"*User is not an owner of the \
                                       slackr, or an owner of this channel*"):
        ch_addowner(data, user2['token'],
                    channel['channel_id'], user1['u_id'])

    # ValueError
    with pytest.raises(ValueError, match=r"*Invalid Channel ID*"):
        ch_addowner(ch_addowner(data, user_admin['token'],
                                channel['channel_id'] - 123, user1['u_id']))

    with pytest.raises(ValueError, match=r"*User already an owner of \
                                            the channel*"):
        ch_addowner(ch_addowner(data, user_admin['token'],
                                channel['channel_id'], user1['u_id']))


# Testing valid input for channel_removeowner
def test_channel_removeowner_ok():
    data = getdata()
    user_admin = data['users'][0]
    user1 = data['users'][1]
    channel = ch_create(data, user_admin['token'], '12345', True)

    ch_join(data, user1['token'], channel['channel_id'])

    ch_addowner(data, user_admin['token'], channel['channel_id'],
                user1['u_id'])
    ch_removeowner(data, user_admin['token'], channel['channel_id'],
                   user1["u_id"])

    channel_profile = ch_details(data, user_admin['token'],
                                 channel['channel_id'])
    owner_list = channel_profile["owner_members"]

    # if user1["u_id"] is in the owner list
    # Means channel_removeowner is not working
    if user1['u_id'] in owner_list:
        exist = 0
    else:
        exist = 1
    assert exist == 1

    assert owner_list[0]["u_id"] == user_admin["u_id"]


# Testing invalid input for channel_removeowner
def test_channel_removeowner_bad():
    data = getdata()
    user_admin = data['users'][0]
    user1 = data['users'][1]
    user2 = data['users'][2]
    channel = ch_create(data, user_admin['token'], '12345', True)

    ch_join(data, user1['token'], channel['channel_id'])
    ch_join(data, user2['token'], channel['channel_id'])

    ch_addowner(data, user_admin['token'], channel['channel_id'],
                user1['u_id'])
    # ValueError
    with pytest.raises(ValueError, match=r"*Invalid Channel ID*"):
        ch_removeowner(data, user_admin['token'], channel['channel_id'] - 123,
                       user1['u_id'])

    with pytest.raises(ValueError, match=r"*User is not an owner of \
                                           the channel*"):
        ch_removeowner(data, user_admin['token'], channel['channel_id'],
                       user2['u_id'])

    # AccessError
    with pytest.raises(AccessError, match=r"*User is not an owner of the \
                       slackr, or an owner of this channel*"):
        ch_addowner(data, user2['u_id'], channel['channel_id'], user1['u_id'])


# Testing valid input for channels_list
def test_channels_list():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    channel1 = channels_create(auth_key_admin["token"], "12345", True)
    channel2 = channels_create(auth_key_admin["token"], "123asdf45", True)
    
    auth_key = auth_register("1234asd56@gmail.com", "123456fs789", "hh123h", "asasddf")
    channel3 = channels_create(auth_key["token"], "12345", True)
    channel4 = channels_create(auth_key["token"], "123asasxzdf45", True)
    
    data = getdata()
    user_admin = data['users'][0]
    channel1 = ch_create(data, user_admin['token'], '12345', True)
    channel2 = ch_create(data, user_admin['token'])
    
    channels = channels_list(auth_key["token"])
    assert channels[0]["id"] == channel1["id"]
    assert channels[0]["name"] == "12345"
    
    assert channels[1]["id"] == channel2["id"]
    assert channels[0]["name"] == "123asdf45"
    
    assert len(channels) == 2

# Testing valid input for channels_listall
def test_channels_listall():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")

    channel1 = channels_create(auth_key_admin["token"], "12345", True)
    channel2 = channels_create(auth_key_admin["token"], "123asdf45", True)
    
    auth_key = auth_register("1234asd56@gmail.com", "123456fs789", "hh123h", "asasddf")
    channel3 = channels_create(auth_key["token"], "12345", True)
    channel4 = channels_create(auth_key["token"], "123aszxcdf45", True)
    channel5 = channels_create(auth_key["token"], "123asd12f45", False)
    
    channels = channels_listall(auth_key_admin["token"])

    assert channels[0]["id"] == channel1["id"]
    assert channels[0]["name"] == "12345"
    
    assert channels[1]["id"] == channel2["id"]
    assert channels[1]["name"] == "123asdf45"
    
    assert channels[2]["id"] == channel3["id"]
    assert channels[2]["name"] == "12345"
    
    assert channels[3]["id"] == channel4["id"]
    assert channels[3]["name"] == "123aszxcdf45"
    
    assert len(channels) == 4

# Testing valid input for channels_create
def test_channels_create_bad():
    data = getdata()
    user = data['users'][0]

    with pytest.raises(ValueError, match=r"The maximum characters of name is \
                                           20."):
        ch_create(data, user['token'], "012345678901234567890123456789", True)
