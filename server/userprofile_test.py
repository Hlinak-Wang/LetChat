from server.user_function import usersetemail, usersetname, usersethandle, getprofile
from server.auth_function import register


def getData():
    data = {
        'users': []
    }
    return data


def test_profile():
    data = getData()
    # Create one user for testing
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')

    # Invalid input
    value, Errormessage = getprofile(data, None, None)
    assert Errormessage == "Invalid token or u_id"

    value, Errormessage = getprofile(data, 'not_valid_token', 'not_valid_u_id')
    assert Errormessage == "User with u_id is not a valid user"

    # Valid input
    value, Errormessage = getprofile(data, auth_key["token"], auth_key["u_id"])
    assert value["email"] == 'email@gmail.com'
    assert value["name_first"] == 'name_first'
    assert value["name_last"] == 'name_last'
    # Assume the default handle is the first_namelast_name
    assert value["handle_str"] == 'name_firstname_last'


def test_setname():
    data = getData()
    # create one user
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')

    # name_first more than 50 characters but not name_last
    first_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    first_short = 'asdfzxcv'

    last_short = 'abcd'
    last_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    # Invalid input
    value, Errormessage = usersetname(data, None, first_long, last_short)
    assert Errormessage == "token doesn't exit"

    value, Errormessage = usersetname(data, auth_key["token"], first_long, last_short)
    assert Errormessage == 'name_first is not between 1 and 50 characters in length'

    value, Errormessage = usersetname(data, auth_key["token"], first_short, last_long)
    assert Errormessage == 'name_last is not between 1 and 50 characters in length'

    value, Errormessage = usersetname(data, 'token_not_registed', first_short, last_short)
    assert Errormessage == 'User with token is not a valid user'

    # Valid input
    usersetname(data, auth_key["token"], first_short, last_short)
    profile, error = getprofile(data, auth_key["token"], auth_key["u_id"])
    assert profile["name_first"] == first_short
    assert profile["name_last"] == last_short


def test_setemail():
    data = getData()
    # Register two user for testing
    auth_key = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')
    auth_key1 = register(data, 'email@gmail.com1', 'password1', 'name_first1', 'name_last1')

    invalid_email = 'dffgfddfsa.com'
    email_used_already = 'email@gmail.com'

    # Invalid input
    value, Errormessage = usersetemail(data, None, invalid_email)
    assert Errormessage == "token doesn't exit"

    value, Errormessage = usersetemail(data, auth_key["token"], invalid_email)
    assert Errormessage == 'Email entered is not a valid email'

    value, Errormessage = usersetemail(data, auth_key["token"], email_used_already)
    assert Errormessage == 'Email address is already being used by another user'

    value, Errormessage = usersetemail(data, 'token_not_registed', '123@gmail.com')
    assert Errormessage == 'User with token is not a valid user'

    # Valid input
    value, Errormessage = usersetemail(data, auth_key["token"], 'newemail@gmail.com')
    profile, error = getprofile(data, auth_key["token"], auth_key["u_id"])
    assert profile["email"] == 'newemail@gmail.com'


def test_sethandle():
    data = getData()
    user = register(data, 'email@gmail.com', 'password', 'name_first', 'name_last')
    other_user = register(data, 'other@gmail.com', 'password', 'first', 'last')

    handle_long = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
    handle_normal = 'normal'

    handle_used = 'handle_str'
    usersethandle(data, other_user['token'], handle_used)

    # Invalid input
    # handle_str is no more than 20 charaters
    value, Errormessage = usersethandle(data, None, handle_normal)
    assert Errormessage == "token doesn't exit"

    value, Errormessage = usersethandle(data, user["token"], handle_long)
    assert Errormessage == "handle_str must be between 3 and 20"

    value, Errormessage = usersethandle(data, user["token"], handle_used)
    assert Errormessage == "handle is already used by another user"

    value, Errormessage = usersethandle(data, 'token_not_registed', handle_normal)
    assert Errormessage == "User with token is not a valid user"

    # Valid input
    value, Errormessage = usersethandle(data, user["token"], 'testing')
    profile, error = getprofile(data, user["token"], user["u_id"])
    assert profile["handle_str"] == 'testing'


def test_uploadphoto():
    # Create one user for testing
    pass
