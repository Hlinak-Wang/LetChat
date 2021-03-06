from server.channel_function import (
    ch_create,
    ch_invite,
    ch_details,
    ch_join_leave,
    ch_add_remove_owner,
    ch_lists_listall,
    fun_message
)
from server.message_function import send_message
from server.auth_functions import register
from server.extra_function import (
    standup_message,
    standup_begin
)

from server.Data_class import Data


# initial state of testing
def getdata():
    data = Data()
    ch_owner = register(data, 'test@test.com', 'testtest', 'test', 'test',
                        'http://127.0.0.1:5555/')
    ch_member = register(data, 'test2@test2.com', 'test2test2', 'test2',
                         'test2', 'http://127.0.0.1:5555/')
    register(data, 'tests2@tests2.com', 'tests2', 'not in channel', 'test',
             'http://127.0.0.1:5555/')
    channel1 = ch_create(data, ch_owner['token'], 'ch_test', True)
    ch_join_leave(data, ch_member['token'], channel1['channel_id'], 'join')
    # data, token, channel_id, message, time_create=datetime.now()
    send_message(data, ch_owner['token'], channel1['channel_id'], 'test')
    send_message(data, ch_member['token'], channel1['channel_id'], 'test2')
    return data


def get_host():
    return 'http://127.0.0.1:5555/'


# Testing valid input for channel_invite
def test_channel_invite_ok():
    data = getdata()
    host = get_host()
    user = data.users_group[0]
    user1 = data.users_group[1]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user.token, '12345', True)
    # it takes in data, token, u_id and channel_id
    ch_invite(data, user.token, user1.u_id, channel['channel_id'])

    # Check the user is successfully added into channel
    # it takes in data, token and channel_id
    channel_profile = ch_details(data, user.token, channel['channel_id'], host)
    member_list = channel_profile['all_members']
    assert member_list[0]['u_id'] == user.u_id
    assert member_list[1]['u_id'] == user1.u_id


# Testing invalid input for channel_invite
def test_channel_invite_bad():
    data = getdata()

    user = data.users_group[0]
    user1 = data.users_group[1]
    user2 = data.users_group[2]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user.token, '12345', True)
    res1 = ch_invite(data, user.token, user1.u_id, '2222')
    assert res1 == {'ValueError': 'Invalid channel id'}

    res2 = ch_invite(data, user.token, '55555', channel['channel_id'])
    assert res2 == {'ValueError': 'Invalid u_id'}

    res3 = ch_invite(data, user2.token, user2.u_id,
                     channel['channel_id'])
    assert res3 == {'AccessError': 'The authorised user is not already a \
member of the channel'}
    ch_invite(data, user.token, user1.u_id, channel['channel_id'])
    res4 = ch_invite(data, user.token, user1.u_id, channel['channel_id'])
    assert res4 == {'AccessError': 'The invite user is already a member of the\
 channel'}


# Testing valid input for channel_details
def test_channel_details_ok():
    data = getdata()
    host = get_host()
    user = data.users_group[0]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user.token, '12345', True)

    channel_profile = ch_details(data, user.token, channel['channel_id'], host)
    # Checking the output of channel detail
    assert channel_profile['name'] == "12345"

    owner_list = channel_profile["owner_members"]
    assert owner_list[0]['u_id'] == user.u_id

    member_list = channel_profile["all_members"]
    assert member_list[0]['u_id'] == user.u_id


# Testing invalid input for channel detail
def test_channel_details_bad():
    data = getdata()
    host = get_host()
    user = data.users_group[0]
    user1 = data.users_group[2]
    # it takes in data, token, channel_name and is_public
    channel = ch_create(data, user.token, '12345', True)

    res1 = ch_details(data, user.token, '123456', host)
    assert res1 == {'ValueError': 'Invalid channel id'}

    res2 = ch_details(data, user1.token, channel['channel_id'], host)
    assert res2 == {'AccessError': 'User is not a member of Channel'}


# Testing valid input for channel_message
def test_channel_messages_ok():
    data = getdata()
    user = data.users_group[0]
    channel = ch_create(data, user.token, '12345', True)
    send_message(data, user.token, channel['channel_id'], 'testing')
    message_channel = fun_message(data, user.token,
                                  channel['channel_id'], 0)
    channel1 = data.channels_group[0]
    message_channel1 = fun_message(data, user.token,
                                   channel1.channel_id, 0)
    # Checking the output
    assert message_channel['start'] == 0
    assert message_channel['end'] == -1
    messages = message_channel['messages']
    assert messages[0]['message'] == 'testing'
    assert messages[0]['u_id'] == user.u_id

    assert message_channel1['start'] == 0
    assert message_channel1['end'] == -1
    messages1 = message_channel1['messages']
    assert messages1[1]['message'] == 'test'
    assert messages1[1]['u_id'] == user.u_id
    standup_begin(data, user.token, channel['channel_id'], 10)
    for i in range(0, 25):
        send_message(data, user.token, channel['channel_id'], 'another test')
        send_message(data, user.token, channel['channel_id'], 'again')
        standup_message(data, user.token, channel['channel_id'], 'testing')
        i = i + 1
    message_channel2 = fun_message(data, user.token,
                                   channel['channel_id'], 0)
    assert message_channel2['start'] == 0
    assert message_channel2['end'] == 50


# Testing invalid input for channel_message
def test_channel_messages_bad():
    data = getdata()
    user = data.users_group[0]
    user1 = data.users_group[1]
    channel = ch_create(data, user.token, '12345', True)

    # ValueError
    long_message = ""
    for i in range(0, 1010):
        long_message += str(i)

    res1 = send_message(data, user.token, channel['channel_id'], long_message)
    assert res1 == {"ValueError": "Message is more than 1000 characters"}

    res2 = fun_message(data, user.token, channel['channel_id'] - 123, 0)
    assert res2 == {'ValueError': 'Channel ID is not a valid channel'}

    res3 = fun_message(data, user.token, channel['channel_id'], 999999999)
    assert res3 == {'ValueError': 'start is greater than or equal to the total\
 number of messages in the channel'}

    # AccessError
    res4 = send_message(data, user.token, 10, 'testing')
    assert res4 == {'AccessError': 'the authorised user has not joined the \
channel they are trying to post to'}

    res5 = fun_message(data, user1.token, channel['channel_id'], 0)
    assert res5 == {'AccessError': 'when:  the authorised user has not joined \
the channel they are trying to post to'}


# Testing valid input for channel_leave
def test_channel_leave_ok():
    data = getdata()
    host = get_host()
    user = data.users_group[0]
    user1 = data.users_group[1]
    # it takes in data, token, channel_name and is_public and return channel_id
    channel = ch_create(data, user.token, '12345', True)
    # user1 join to the channel
    ch_join_leave(data, user1.token, channel['channel_id'], 'join')
    # add user1 to be the owner of the channel
    ch_add_remove_owner(data, user.token, channel['channel_id'],
                        user1.u_id, 'add')
    # user1 leave the channel
    ch_join_leave(data, user1.token, channel['channel_id'], 'leave')

    # Check the member in channel
    channel_profile = ch_details(data, user.token, channel['channel_id'], host)
    owner_list = channel_profile['owner_members']
    member_list = channel_profile['all_members']
    assert len(owner_list) == 1
    assert len(member_list) == 1


# Testing invalid input for channel_leave
def test_channel_leave_bad():
    data = getdata()
    user = data.users_group[0]
    # it takes in data, token, channel_name and is_public and return channel_id
    ch_create(data, user.token, '12345', True)

    res = ch_join_leave(data, user.token, 10, 'leave')
    assert res == {'ValueError': 'Channel ID is invalid'}


# Testing valid input for channel_join
def test_channel_join_ok():
    data = getdata()
    host = get_host()
    user = data.users_group[0]
    channel = ch_create(data, user.token, '12345', True)
    user2 = data.users_group[1]
    ch_join_leave(data, user2.token, channel['channel_id'], 'join')
    channel_profile = ch_details(data, user2.token, channel['channel_id'],
                                 host)

    # Check the new user has join the channel
    member_list = channel_profile["all_members"]
    assert member_list[0]['u_id'] == user.u_id
    assert member_list[1]['u_id'] == user2.u_id


# Testing invalid input for channel_join
def test_channel_join_bad():
    data = getdata()
    user = data.users_group[0]
    channel = ch_create(data, user.token, '12345', True)
    user2 = data.users_group[1]
    # ValueError
    res1 = ch_join_leave(data, user2.token, channel['channel_id'] - 123,
                         'join')
    assert res1 == {'ValueError': 'Channel ID is invalid'}

    # AccessError
    channel2 = ch_create(data, user.token, '12345', False)
    res2 = ch_join_leave(data, user2.token, channel2['channel_id'], 'join')
    assert res2 == {'AccessError': 'The channel is private'}

    res3 = ch_join_leave(data, user.token, channel['channel_id'], 'join')
    assert res3 == {'AccessError': 'Already a member of that channel'}


# Testing valid input for channel_addowner
def test_channel_addowner_ok():
    data = getdata()
    host = get_host()
    user = data.users_group[0]
    channel = ch_create(data, user.token, '12345', True)
    user2 = data.users_group[2]
    ch_join_leave(data, user2.token, channel['channel_id'], 'join')

    ch_add_remove_owner(data, user.token, channel['channel_id'], user2.u_id,
                        'add')
    channel_profile = ch_details(data, user.token, channel['channel_id'], host)
    owner_list = channel_profile['owner_members']
    # Checking there is two owner in this channel
    assert owner_list[0]['u_id'] == user.u_id
    assert owner_list[1]['u_id'] == user2.u_id


# Testing invalid input for channel_addowner
def test_channel_addowner_bad():
    data = getdata()
    user_admin = data.users_group[0]
    user1 = data.users_group[1]
    user2 = data.users_group[2]
    channel = ch_create(data, user_admin.token, '12345', True)
    ch_join_leave(data, user1.token, channel['channel_id'], 'join')

    ch_join_leave(data, user2.token, channel['channel_id'], 'join')
    # AccessError
    res1 = ch_add_remove_owner(data, user2.token, channel['channel_id'],
                               user1.u_id, 'add')
    assert res1 == {'AccessError': 'User is not an owner of the slackr or this\
 channel'}

    res2 = ch_add_remove_owner(data, user_admin.token, channel['channel_id'],
                               99876, 'add')
    assert res2 == {'AccessError': 'Not a member of this channel'}

    # ValueError
    invalid_ch_id = channel['channel_id'] - 123
    res3 = ch_add_remove_owner(data, user_admin.token, invalid_ch_id,
                               user1.u_id, 'add')
    assert res3 == {'ValueError': 'Invalid Channel ID'}
    ch_add_remove_owner(data, user_admin.token, channel['channel_id'],
                        user1.u_id, 'add')
    res4 = ch_add_remove_owner(data, user_admin.token, channel['channel_id'],
                               user1.u_id, 'add')
    assert res4 == {'ValueError': 'User is already an owner of the channel'}


# Testing valid input for channel_removeowner
def test_channel_removeowner_ok():
    data = getdata()
    host = get_host()
    user_admin = data.users_group[0]
    user1 = data.users_group[1]
    channel = ch_create(data, user_admin.token, '12345', True)

    ch_join_leave(data, user1.token, channel['channel_id'], 'join')

    ch_add_remove_owner(data, user_admin.token, channel['channel_id'],
                        user1.u_id, 'add')
    ch_add_remove_owner(data, user_admin.token, channel['channel_id'],
                        user1.u_id, 'remove')

    channel_profile = ch_details(data, user_admin.token,
                                 channel['channel_id'], host)
    owner_list = channel_profile["owner_members"]
    # if user1["u_id"] is in the owner list
    # Means channel_removeowner is not working
    exist = 0
    if user1.u_id not in owner_list:
        exist = 1
    assert exist == 1

    assert owner_list[0]['u_id'] == user_admin.u_id


# Testing invalid input for channel_removeowner
def test_channel_removeowner_bad():
    data = getdata()
    user_admin = data.users_group[0]
    user1 = data.users_group[1]
    user2 = data.users_group[2]
    channel = ch_create(data, user_admin.token, '12345', True)

    ch_join_leave(data, user1.token, channel['channel_id'], 'join')
    ch_join_leave(data, user2.token, channel['channel_id'], 'join')

    ch_add_remove_owner(data, user_admin.token, channel['channel_id'],
                        user1.u_id, 'remove')
    # ValueError
    invalid_ch_id = channel['channel_id'] - 123
    res1 = ch_add_remove_owner(data, user_admin.token, invalid_ch_id,
                               user1.u_id, 'remove')
    assert res1 == {'ValueError': 'Invalid Channel ID'}

    res2 = ch_add_remove_owner(data, user_admin.token, channel['channel_id'],
                               user2.u_id, 'remove')
    assert res2 == {'ValueError': 'User is not an owner of the channel'}
    ch_add_remove_owner(data, user_admin.token, channel['channel_id'],
                        user1.u_id, 'remove')
    # AccessError
    res3 = ch_add_remove_owner(data, user2.token, channel['channel_id'],
                               user1.u_id, 'remove')
    assert res3 == {'AccessError': 'User is not an owner of the slackr or \
this channel'}


# Testing valid input for channels_list
def test_channels_list():
    data = getdata()
    user_admin = data.users_group[0]
    # channel1
    ch_create(data, user_admin.token, 'ch_1', True)
    # channel2
    ch_create(data, user_admin.token, 'ch_2', True)

    user1 = data.users_group[1]
    channel3 = ch_create(data, user1.token, 'ch_3', True)
    channel4 = ch_create(data, user1.token, 'ch_4', True)

    channels = ch_lists_listall(data, user1.token, 'lists')

    assert channels['channels'][1]['channel_id'] == channel3['channel_id']
    assert channels['channels'][1]['name'] == 'ch_3'

    assert channels['channels'][2]['channel_id'] == channel4['channel_id']
    assert channels['channels'][2]['name'] == 'ch_4'

    assert len(channels['channels']) == 3


# Testing valid input for channels_listall
def test_channels_listall():
    data = getdata()
    user_admin = data.users_group[0]
    user1 = data.users_group[1]
    channel1 = ch_create(data, user_admin.token, '12345', True)
    channel2 = ch_create(data, user_admin.token, '123asdf45', True)
    channel3 = ch_create(data, user1.token, '12345', True)
    channel4 = ch_create(data, user1.token, '123aszxcdf45', True)
    channel5 = ch_create(data, user1.token, '123asd12f45', False)

    channels = ch_lists_listall(data, user1.token, 'listall')

    assert channels['channels'][1]['channel_id'] == channel1['channel_id']
    assert channels['channels'][1]['name'] == '12345'

    assert channels['channels'][2]['channel_id'] == channel2['channel_id']
    assert channels['channels'][2]['name'] == '123asdf45'

    assert channels['channels'][3]['channel_id'] == channel3['channel_id']
    assert channels['channels'][3]['name'] == '12345'

    assert channels['channels'][4]['channel_id'] == channel4['channel_id']
    assert channels['channels'][4]['name'] == '123aszxcdf45'

    assert channels['channels'][5]['channel_id'] == channel5['channel_id']
    assert channels['channels'][5]['name'] == '123asd12f45'
    assert len(channels['channels']) == 6


# Testing valid input for channels_create
def test_channels_create_bad():
    data = getdata()
    user = data.users_group[0]
    res1 = ch_create(data, user.token, "012345678901234567890123456789",
                     True)
    assert res1 == {'ValueError': 'The maximum characters of name is 20.'}

    res2 = ch_create(data, 'jwerjhlw', '1128', True)
    assert res2 == {'ValueError': 'token not valid'}
