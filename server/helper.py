import re
import hashlib
from datetime import datetime

def authorise(function):
    def wrapper(*args):
        if len(args) >= 2:
            data = args[0]
            token = args[1]
            user = data.get_element('users_group', 'token', token)
            if user is not None:
                new_args = list(args)
                new_args[1] = user
                args = tuple(new_args)
                return function(*args)
            else:
                return {'ValueError': 'token not valid'}

    return wrapper


def check_valid_email(email):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if not re.search(regex, email):
        return {'ValueError': "This email is not valid"}
    return {}


def check_valid_password(password):
    if len(password) < 6:
        return {'ValueError': "This password is too short"}
    return {}


def check_name(name_first, name_last):
    if (len(name_first) < 1) or (len(name_last) < 1):
        return {'ValueError': "First name or last name too short"}
    elif len(name_first) > 50 or (len(name_last) > 50):
        return {'ValueError': "First name or last name too long"}

    return {}


def user_login_verify(data, email, password):
    for user in data.users_group:
        if user.email == email:
            if user.password == hashlib.sha256(password.encode("utf-8")).hexdigest():
                return user
            else:
                return {'ValueError': "Incorrect password entered"}
    return {'ValueError': "This email does not belong to a user"}


def get_channel_message(data, channel_id, u_id, start):
    channel_message = []
    counter = 0
    end = start
    time_now = datetime.now().timestamp()
    for message in data.messages_group[start:]:
        if message.channel_id == channel_id and message.time_created <= time_now:
            channel_message.append(message.get_message_info(u_id))
            counter += 1
        end += 1
        if counter >= 50:
            return {
                'messages': channel_message,
                'start': start,
                'end': end
            }
    return {
        'messages': channel_message,
        'start': start,
        'end': -1
    }
