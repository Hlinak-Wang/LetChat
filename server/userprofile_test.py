def test_profile():
    valid_email = '1234545@abc.com'
    valid_password = 21345123
    token = auth_login(valid_email,valid_password)
    email, user_profile(token)
    pass

def test_setname():

    token = 'asdf'

    #name_first more than 50 characters but not name_last
    name_first = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    name_last = 'abcd'
    assert user_profile_setname(token, name_first, name_last) == 'First name more than 50 characters'

    #name_last more than 50 characters but not name_first
    name_first = 'abcd'
    name_first = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    assert user_profile_setname(token, name_first, name_last) == 'Last name more than 50 characters'


def test_setemail():


    pass

def test_sethandle():

    pass

def test_uploadphoto():


    pass