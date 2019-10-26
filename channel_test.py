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
        ch_listall,
        fun_message,
        fun_send
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
                 'channel_involve': [0]  # channel_id
                 },
                {'u_id': 1234,
                 'name_first': 'test2',
                 'name_last': 'test2',
                 'token': '123456',
                 'handle_str': 'testtest2',
                 'email': 'test2@test2.com',
                 'password': 'test2',
                 'permission_id': 3,
                 'channel_involve': [0]  # channel_id
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
                'channel_id': 0,
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
                        'channel_id': 0
                    },
                    {
                        'message': 'test2',
                        'u_id': 1234,
                        'reacts': [{'react_id': 1, 'u_ids': []}],
                        'is_pinned': False,
                        'time_created': '10/20/2019, 23:24:33',
                        'message_id': 0,
                        'channel_id': 0
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
    user1 = data['users'][1]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user['token'], '12345', True)
    # it takes in data, token, u_id and channel_id
    ch_invite(data, user['token'], user1['u_id'], channel['channel_id'])

    # Check the user is successfully added into channel
    # it takes in data, token and channel_id
    channel_profile = ch_details(data, user['token'], channel['channel_id'])
    member_list = channel_profile['all_members']
    assert member_list[0]['u_id'] == user['u_id']
    assert member_list[1]['u_id'] == user1['u_id']


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

    res3 = ch_invite(data, user2['token'], user2['u_id'], channel['channel_id'])
    assert res3 == {'AccessError': 'The authorised user is not already a member of the channel'}
    ch_invite(data, user['token'], user1['u_id'], channel['channel_id'])
    res4 = ch_invite(data, user['token'], user1['u_id'], channel['channel_id'])
    assert res4 == {'AccessError': 'The invite user is already a member of the channel'}


# Testing valid input for channel_details
def test_channel_details_ok():
    data = getdata()
    user = data['users'][0]
    print(user)
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user['token'], '12345', True)

    channel_profile = ch_details(data, user['token'], channel['channel_id'])
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
    user1 = data['users'][2]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user['token'], '12345', True)

    res1 = ch_details(data, user['token'], '123456')
    assert res1 == {'ValueError': 'Invalid channel id'}

    res2 = ch_details(data, user1['token'], channel['channel_id'])
    assert res2 == {'AccessError': 'User is not a member of Channel'}


# Testing valid input for channel_message
def test_channel_messages_ok():
    data = getdata()
    user = data['users'][0]
    channel = ch_create(data, user['token'], '12345', True)
    fun_send(data, user['token'], channel['channel_id'], 'testing')

    message_channel = fun_message(data, user['token'],
                                  channel['channel_id'], 0)
    # Checking the output
    assert message_channel['start'] == 0
    assert message_channel['end'] == -1

    messages = message_channel['messages']
    assert messages[0]['message'] == 'testing'
    assert messages[0]['u_id'] == user['u_id']


# Testing invalid input for channel_message
def test_channel_messages_bad():
    data = getdata()
    user_admin = data['users'][0]
    user1 = data['users'][1]
    channel = ch_create(data, user_admin['token'], '12345', True)
    
    # ValueError
    res1 = fun_message(data, user_admin['token'], channel['channel_id'] - 123, 0)
    assert res1 == {'ValueError': 'Channel ID is not a valid channel'}
        
    res2 = fun_message(data, user_admin['token'], channel['channel_id'], 999999999)
    assert res2 == {'ValueError': 'start is greater than or equal to the total number of messages in the channel'}

    # AccessError
    res3 = fun_message(data, user1['token'], channel['channel_id'], 0)
    assert res3 == {'AccessError': 'when:  the authorised user has not joined the channel they are trying to post to'}        


# Testing valid input for channel_leave
def test_channel_leave_ok():
    data = getdata()
    user = data['users'][0]
    user1 = data['users'][1]
    # it takes in data, token, channel_name and is_public and return channel_id
    channel = ch_create(data, user['token'], '12345', True)

    ch_join(data, user1['token'], channel['channel_id'])
    ch_leave(data, user1['token'], channel['channel_id'])

    # Check the member in channel
    channel_profile = ch_details(data, user['token'], channel['channel_id'])
    member_list = channel_profile['all_members']
    assert member_list[0]["u_id"] == user['u_id']


# Testing invalid input for channel_leave
def test_channel_leave_bad():
    data = getdata()
    user = data['users'][0]
    # it takes in data, token, channel_name and is_public and return channel_id
    channel = ch_create(data, user['token'], '12345', True)

    res = ch_leave(data, user['token'], 10)
    assert res == {'ValueError': 'Channel ID is invalid'}


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
    res1 = ch_join(data, user2['token'], channel['channel_id'] - 123)
    assert res1 == {'ValueError': 'Channel ID is invalid'}

    # AccessError
    channel2 = ch_create(data, user['token'], '12345', False)
    res2 = ch_join(data, user2['token'], channel2['channel_id'])
    assert res2 == {'AccessError': 'The channel is private'}


# Testing valid input for channel_addowner
def test_channel_addowner_ok():
    data = getdata()
    user = data['users'][0]
    channel = ch_create(data, user['token'], '12345', True)
    user2 = data['users'][2]
    ch_join(data, user2['token'], channel['channel_id'])

    ch_addowner(data, user['token'], channel['channel_id'], user2['u_id'])
    channel_profile = ch_details(data, user['token'], channel['channel_id'])
    owner_list = channel_profile['owner_members']

    # Checking there is two owner in this channel
    assert owner_list[0]['u_id'] == user['u_id']
    assert owner_list[1]['u_id'] == user2['u_id']


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
    res1 = ch_addowner(data, user2['token'], channel['channel_id'],
                       user1['u_id'])
    assert res1 == {'AccessError': 'User is not an owner of the slackr or this channel'}

    # ValueError
    res2 = ch_addowner(data, user_admin['token'], channel['channel_id'] - 123,
                       user1['u_id'])
    assert res2 == {'ValueError': 'Invalid Channel ID'}
    ch_addowner(data, user_admin['token'], channel['channel_id'],
                user1['u_id'])
    res3 = ch_addowner(data, user_admin['token'], channel['channel_id'],
                       user1['u_id'])
    assert res3 == {'ValueError': 'User is already an owner of the channel'}


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
    res1 = ch_removeowner(data, user_admin['token'],
                          channel['channel_id'] - 123, user1['u_id'])
    assert res1 == {'ValueError': 'Invalid Channel ID'}

    res2 = ch_removeowner(data, user_admin['token'], channel['channel_id'],
                          user2['u_id'])
    assert res2 == {'ValueError': 'User is not an owner of the channel'}

    # AccessError
    res3 = ch_removeowner(data, user2['token'], channel['channel_id'],
                       user1['u_id'])
    assert res3 == {'AccessError': 'User is not an owner of the slackr or this channel'}


# Testing valid input for channels_list
def test_channels_list():
    data = getdata()
    user_admin = data['users'][0]
    channel1 = ch_create(data, user_admin['token'], 'ch_1', True)
    channel2 = ch_create(data, user_admin['token'], 'ch_2', True)
    
    user1 = data['users'][1]
    channel3 = ch_create(data, user1['token'], 'ch_3', True)
    channel4 = ch_create(data, user1['token'], 'ch_4', True)
    
    channels = ch_lists(data, user1['token'])

    assert channels['channels'][1]['channel_id'] == channel3['channel_id']
    assert channels['channels'][1]['name'] == 'ch_3'
    
    assert channels['channels'][2]['channel_id'] == channel4['channel_id']
    assert channels['channels'][2]['name'] == 'ch_4'

    assert len(channels['channels']) == 3

# Testing valid input for channels_listall
def test_channels_listall():
    data = getdata()
    user_admin = data['users'][0]
    user1 = data['users'][1]
    channel1 = ch_create(data, user_admin['token'], '12345', True)
    channel2 = ch_create(data, user_admin['token'], '123asdf45', True)
    channel3 = ch_create(data, user1['token'], '12345', True)
    channel4 = ch_create(data, user1['token'], '123aszxcdf45', True)
    channel5 = ch_create(data, user1['token'], '123asd12f45', False)
    
    channels = ch_listall(data, user_admin['token'])

    assert channels['channels'][1]['channel_id'] == channel1['channel_id']
    assert channels['channels'][1]['name'] == '12345'
    
    assert channels['channels'][2]['channel_id'] == channel2['channel_id']
    assert channels['channels'][2]['name'] == '123asdf45'
    
    assert channels['channels'][3]['channel_id'] == channel3['channel_id']
    assert channels['channels'][3]['name'] == '12345'
    
    assert channels['channels'][4]['channel_id'] == channel4['channel_id']
    assert channels['channels'][4]['name'] == '123aszxcdf45'
    
    assert len(channels['channels']) == 5

# Testing valid input for channels_create
def test_channels_create_bad():
    data = getdata()
    user = data['users'][0]
    res = ch_create(data, user['token'], "012345678901234567890123456789", True)
    assert res == {'ValueError': 'The maximum characters of name is 20.'}
        
