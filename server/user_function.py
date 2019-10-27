import re

# Make a regular expression
# for validating an Email
Regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


# Define a function for
# for validating an Email
def check(email):
    # pass the regualar expression
    # and the string in search() method
    if (re.search(Regex, email)):
        return 1
    return 0

#find user by token, return user if found, return None if not found
def getuser(data, token):

    for user in data['users']:
        if user['token'] == token:
            return user

    return None

#check email status if used return 0 else return 1
def checkemailnotused(data, email):

    for user in data['users']:
        if user['email'] == email:
            return 0

    return 1

#check handle status if used return 0 else return 1
def checkhandlenotused(data, handle):

    for user in data['users']:
        if user['handle_str'] == handle:
            return 0

    return 1

#get user profile by token
def getprofile(data, token, u_id):
    value = None
    wrongmessage = None

    if token is None or u_id is None:
        wrongmessage = "Invalid token or u_id"
        return (value, wrongmessage)

    user = getuser(data, token)

    if user is None:
        wrongmessage = "User with u_id is not a valid user"
        return (value, wrongmessage)

    value = {'email': user['email'],
             'name_first': user['name_first'],
             'name_last': user['name_last'],
             'handle_str': user['handle_str'], }

    return (value, wrongmessage)

#set username by token
def usersetname(data, token, name_first, name_last):
    value = None
    wrongmessage = None

    if token is None:
        wrongmessage = "token doesn't exit"
        return (value, wrongmessage)

    if len(name_first) > 50 or len(name_first) < 0:
        wrongmessage = "name_first is not between 1 and 50 characters in length"
        return (value, wrongmessage)

    if len(name_last) > 50 or len(name_last) < 0:
        wrongmessage = "name_last is not between 1 and 50 characters in length"
        return (value, wrongmessage)

    user = getuser(data, token)

    if user is None:
        wrongmessage = "User with token is not a valid user"
        return (value, wrongmessage)

    user['name_first'] = name_first
    user['name_last'] = name_last

    for channel in data['channels']:
        if channel['channel_id'] in user['channel_involve']:
            for member in channel['user_list']:
                if member['u_id'] == user['u_id']:
                    member['name_first'] = name_first
                    member['name_last'] = name_last
    value = 1

    return (value, wrongmessage)

#set user email by token
def usersetemail(data, token, email):
    value = None
    wrongmessage = None

    if token is None:
        wrongmessage = "token doesn't exit"
        return (value, wrongmessage)

    if check(email) == 0:
        wrongmessage = "Email entered is not a valid email"
        return (value, wrongmessage)

    if checkemailnotused(data, email) == 0:
        wrongmessage = "Email address is already being used by another user"
        return (value, wrongmessage)

    user = getuser(data, token)

    if user is None:
        wrongmessage = "User with token is not a valid user"
        return (value, wrongmessage)

    user['email'] = email

    value = 1

    return (value, wrongmessage)

#set user handle by token
def usersethandle(data, token, handle_str):
    value = None
    wrongmessage = None

    if token is None:
        wrongmessage = "token doesn't exit"
        return (value, wrongmessage)

    if len(handle_str) > 20 or len(handle_str) < 3:
        wrongmessage = "handle_str must be between 3 and 20"
        return (value, wrongmessage)

    if checkhandlenotused(data, handle_str) == 0:
        wrongmessage = "handle is already used by another user"
        return (value, wrongmessage)

    user = getuser(data, token)

    if user is None:
        wrongmessage = "User with token is not a valid user"
        return (value, wrongmessage)

    user['handle_str'] = handle_str

    value = 1

    return (value, wrongmessage)
