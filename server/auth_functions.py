import re
import jwt
from datetime import datetime

# HELPER FUNCTIONS BELOW

SECRET = 'IE4'


def check_valid_email(email):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if not re.search(regex, email):
        return {'ValueError': "This email is not valid"}
    return {}


def check_user_details(data, email, password):
    for user in data['users']:
        if user['email'] == email:
            if user['password'] == password:
                return user
            else:
                return {'ValueError': "Incorrect password entered"}
    return {'ValueError': "This email does not belong to a user"}


def check_valid_password(password):
    if len(password) < 6:
        return {'ValueError': "This password is too short"}
    return {}


def check_already_user(data, email):
    for user in data['users']:
        if user['email'] == email:
            return {'ValueError': "This email is already in use by a user"}
    return {}


def check_name(name_first, name_last):
    if (len(name_first) < 1) or (len(name_last) < 1):
        return {'ValueError': "First name or last name too short"}
    elif len(name_first) > 50 or (len(name_last) > 50):
        return {'ValueError': "First name or last name too long"}

    return {}


def generateToken(first, last):
    payload = {
        'first': first,
        'last': last,
        'time_create': datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
    }
    return str(jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8'))


def generateHandle(data, first, last):
    handle = first + last
    excess = len(handle) - 20
    if excess > 0:
        handle = handle[:20]

    if handleAlreadyExists(data, handle) or len(handle) < 3:
        handle = datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")

    return handle


def handleAlreadyExists(data, handle):
    for user in data['users']:
        if user['handle_str'] == handle:
            return True
    return False


def findUserFromToken(data, token):
    # print("hi")
    for user in data['users']:
        print(user)
        if user['token'] == token:
            return user

    return None


def findUserFromEmail(data, email):
    for user in data['users']:
        if user['email'] == email:
            return user


def find_resetcode(data, reset_code):
    for user in data['users']:
        if user['reset_code'] == reset_code:
            return user
    return None


def decoding_reset_code(reset_code):
    return jwt.decode(reset_code, SECRET, algorithms=['HS256'])


# HELPER FUNCTIONS ABOVE

def login(data, email, password):
    email_check = check_valid_email(email)

    if 'ValueError' in email_check:
        return email_check

    user = check_user_details(data, email, password)

    if 'ValueError' in user:
        return user

    token = generateToken(user['name_first'], user['name_last'])
    user['token'] = token

    return {'u_id': user['u_id'], 'token': token}


def logout(data, token):
    user = findUserFromToken(data, token)
    # print(user)
    if user is not None:
        user['token'] = None
        is_success = True
    else:
        is_success = False
    return {'is_sucess': is_success}


def register(data, email, password, name_first, name_last):
    email_check = check_valid_email(email)
    password_check = check_valid_password(password)
    name_check = check_name(name_first, name_last)
    user_check = check_already_user(data, email)

    if 'ValueError' in email_check:
        return email_check

    if 'ValueError' in password_check:
        return password_check

    if 'ValueError' in name_check:
        return name_check

    if 'ValueError' in user_check:
        return user_check

    u_id = len(data['users'])

    token = generateToken(name_first, name_last)

    handle = generateHandle(data, name_first, name_last)

    if u_id == 0:
        permission = 1
    else:
        permission = 3

    data['users'].append({
        'u_id': u_id,
        'name_first': name_first,
        'name_last': name_last,
        'token': token,
        'handle_str': handle,
        'email': email,
        'password': password,
        'permission_id': permission,
        'channel_involve': [],
        'reset_code': None
    })

    return {'u_id': u_id, 'token': token}


def reset_request(data, email):
    user = findUserFromEmail(data, email)

    code = jwt.encode({'email': email}, SECRET, algorithm='HS256').decode('utf-8')
    user['reset_code'] = code

    return code


def reset(data, reset_code, new_password):
    user = find_resetcode(data, reset_code)

    if user is None:
        return {'ValueError': "This is not a valid reset code"}

    return_dictionary = decoding_reset_code(reset_code)

    email = return_dictionary['email']

    if 'ValueError' in check_valid_password(new_password):
        return check_valid_password(new_password)

    check_valid_password(new_password)
    user['password'] = new_password
    user['reset_code'] = None

    return {}
