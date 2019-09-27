import objectToTest as ot

def test_setname():

    token = 'asdf'

    #name_first more than 50 characters but not name_last
    name_first = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    name_last = 'abcd'
    assert ot.user_profile_setname(token, name_first, name_last) == 'First name more than 50 characters'

    #name_last more than 50 characters but not name_first
    name_first = 'abcd'
    name_first = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    assert ot.user_profile_setname(token, name_first, name_last) == 'Last name more than 50 characters'

    #name_last and name_first are both less than 50 characters
    name_first = 'asdf'
    name_last = 'xzv'
    assert ???

def test_setemail():
    token = 'asdf'
    #invalid email
    invalid_email = 'dffgfddfsa.com'
    assert ot.user_profile_setemail(token,invalid_email) == 'Invalid email'

    #email is already being used by other
    invalid_email = '1234567@gmail.com'
    assert ot.user_profile_setemail(token,invalid_email) == 'Email is already being used by other'


def test_sethandle():

    token = 'asdf'

    #handle_str with over 20 characters
    handle_str = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' 
    assert ot.user_profile_sethandle(token, handle_str) = 'handle_str is more than 20 characters'

    ???

def test_uploadphoto():



    pass

def test_profile():
    valid_email = '1234545@abc.com'
    valid_password = 21345123
    token = ot.auth_login(valid_email,valid_password)
    email, user_profile(token)