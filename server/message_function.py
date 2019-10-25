# UTF-8
"""
Date start:11/10/2019
Author: Shili Wang
"""

from datetime import datetime, timedelta, timezone, date


def find_user(data, token):
    for user in data['users']:
        if user['token'] == token:
            return user

    return None


def find_channel(data, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    return None


def find_message_channel(data, message_id):
    for channel in data['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return message, channel

    return None, None


def find_ownership(user_list, member):
    for user in user_list:
        if user['u_id'] == member['u_id']:
            return user['is_owner']
    return None


def find_react(react_list, react_id):
    for react in react_list:
        if react['react_id'] == react_id:
            return react
    return None


def send_message_buffer(data):
    time_now = datetime.now()
    for message in data['message_buffer'][:]:
        time_send = datetime.strptime(message['time_created'],  "%H:%M")
        channel = find_channel(data, message['channel_id'])
        if time_send < time_now:
            channel['messages'].append(message)
            data['message_buffer'].remove(message)


def fun_send_late(data, token, channel_id, message, time_create):
    """ Send message """
    if len(message) > 1000:
        return {"ValueError": "Message is more than 1000 characters"}

    user = find_user(data, token)
    if user is None:
        return {'AccessError': 'User not exist'}

    if channel_id not in user['channel_involve']:
        return {'AccessError': 'the authorised user has not joined the channel they are trying to post to'}

    time_send = datetime.strptime(time_create, "%H:%M").time()
    time_send = datetime.combine(date.today(), time_send)

    if timedelta.total_seconds(time_send - datetime.now()) < 0:
        return {'ValueError': 'Time sent is a time in the past'}

    message_late = {
        'u_id': user['u_id'],
        'message_id': data['message_counter'],
        'message': message,
        'reacts': [{'react_id': 1, 'u_ids': []}],
        'is_pinned': False,
        'time_created': time_send.replace(tzinfo=timezone.utc).timestamp(),
        'channel_id': channel_id
    }
    # assume m_id depend on the number of message been sent
    data['message_buffer'].append(message_late)

    data['message_counter'] += 1
    return {'message_id': data['message_counter'] - 1}


def fun_send(data, token, channel_id, message):
    """ Send message """
    if len(message) > 1000:
        return {"ValueError": "Message is more than 1000 characters"}

    user = find_user(data, token)

    if channel_id not in user['channel_involve']:
        return {'AccessError': 'the authorised user has not joined the channel they are trying to post to'}

    channel = find_channel(data, channel_id)

    # assume m_id depend on the number of message been sent
    time_send = datetime.now()
    channel['messages'].insert(0, {
        'u_id': user['u_id'],
        'message_id': data['message_counter'],
        'message': message,
        'time_created': time_send.replace(tzinfo=timezone.utc).timestamp(),
        'reacts': [{'react_id': 1, 'u_ids': []}],
        'is_pinned': False,
    })
    data['message_counter'] += 1
    return {'message_id': data['message_counter'] - 1}


def fun_remove(data, token, message_id):
    """ assume remove the last one """
    user = find_user(data, token)
    message, channel = find_message_channel(data, message_id)

    if message is None:
        return {'ValueError': 'Message (based on ID) no longer exists'}
    is_owner = find_ownership(channel['user_list'], user)

    if user['u_id'] != message['u_id']:
        if not is_owner or user['permission_id'] == 3:
            return {
                'AccessError': 'permission denied'
            }

    channel['messages'].remove(message)
    return {}


def fun_edit(data, token, message_id, message_edit):
    user = find_user(data, token)
    message, channel = find_message_channel(data, message_id)
    if message is None:
        return {'ValueError': 'Message (based on ID) no longer exists'}

    is_owner = find_ownership(channel['user_list'], user)

    if user['u_id'] != message['u_id']:
        if not is_owner or user['permission_id'] == 3:
            return {
                'AccessError': 'permission denied'
            }

    message['message'] = message_edit
    return {}


def fun_react(data, token, message_id, react_id):
    user = find_user(data, token)
    message = find_message_channel(data, message_id)[0]
    if message is None:
        return {'ValueError': 'Message (based on ID) no longer exists'}

    react = find_react(message['reacts'], react_id)

    if react is None:
        return {'ValueError': 'react_id is not a valid React ID'}

    if user['u_id'] in react['u_ids']:
        return {'ValueError': 'user has reacted'}

    react['u_ids'].append(user['u_id'])
    return {}


def fun_unreact(data, token, message_id, react_id):
    user = find_user(data, token)
    message = find_message_channel(data, message_id)[0]
    if message is None:
        return {'ValueError': 'Message (based on ID) no longer exists'}

    react = find_react(message['reacts'], react_id)

    if react is None:
        return {'ValueError': 'react_id is not a valid React ID'}

    if user['u_id'] not in react['u_ids']:
        return {'ValueError': 'user has not reacted'}

    react['u_ids'].remove(user['u_id'])
    return {}


def fun_pin(data, token, message_id):
    user = find_user(data, token)
    message, channel = find_message_channel(data, message_id)

    if message is None:
        return {'ValueError': 'message_id is not a valid message'}

    if channel['channel_id'] not in user['channel_involve']:
        return {'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    if message["is_pinned"]:
        return {"ValueError": "Message with ID message_id is already pinned"}

    if user['permission_id'] == 3:
        return {'ValueError': 'The authorised user is not an admin'}

    message["is_pinned"] = True

    return {}


def fun_unpin(data, token, message_id):
    user = find_user(data, token)
    message, channel = find_message_channel(data, message_id)

    if message is None:
        return {'ValueError': 'message_id is not a valid message'}

    if channel['channel_id'] not in user['channel_involve']:
        return {'AccessError': 'The authorised user is not a member of the channel that the message is within'}

    if user['permission_id'] == 3:
        return {'ValueError': 'The authorised user is not an admin'}

    if not message["is_pinned"]:
        return {"ValueError": "Message with ID message_id is already unpinned"}
    message["is_pinned"] = False

    return {}
