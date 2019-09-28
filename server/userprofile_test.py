import objectToTest as ot

# This function is to create a valid account
# which would be used in other test_function
def account_register():

    token = ot.auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')

    return token

def test_setname():

    token = account_register()
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
    
    #assert what?

def test_setemail():

    token = account_register()
    #invalid email
    invalid_email = 'dffgfddfsa.com'
    assert ot.user_profile_setemail(token,invalid_email) == 'Invalid email'

    #email is already being used by other
    invalid_email = '1234567@gmail.com'
    assert ot.user_profile_setemail(token,invalid_email) == 'Email is already being used by other'


def test_sethandle():

    token = account_register()

    #handle_str with over 20 characters
    handle_str = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' 
    assert ot.user_profile_sethandle(token, handle_str) = 'handle_str is more than 20 characters'

    #what to do with name_last???

def test_uploadphoto():

    

    pass

def test_profile():

    token = account_register()
    # where can we get u_id??