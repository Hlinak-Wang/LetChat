import objectToTest as ot
import pytest

# This function is to create a valid account
# which would be used in other test_function
def account_register():

    token = ot.auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')

    return token

def test_setname():

    token = account_register()
    #name_first more than 50 characters but not name_last
    first_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    first_short = 'asdfzxcv'

    last_short = 'abcd'
    last_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    with pytest.rasises(ValueError):

        # Name_first is more than 50 characters
        ot.user_profile_setname(token,first_long,last_short)

        # Name_last is more than 50 characters
        ot.user_profile_setname(token, first_short, last_long)

def test_setemail():

    token = account_register()
    token_other = ot.auth_register('adfzcv@gmail.com', 123412, 'HHH', 'LLLL')
    
    invalid_email = 'dffgfddfsa.com'
    email_used_already = 'adfzcv@gmail.com'

    with pytest.rasises(ValueError):

        # Email entered is not a valid email
        ot.user_profile_setemail(token,invalid_email)

        # Email entered is already used by other
        ot.user_profile_setemail(token,email_used_already)

def test_sethandle():

    token = account_register()
    handle_long = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' 
    handle_short = 'abcd'

    with pytest.rasises(ValueError):

        # handle_str is no more than 20 charaters
        ot.user_profile_sethandle(token, handle_long)

        # name_last is more than 50 characters
        #what to do with name_last???

def test_uploadphoto():

    token = account_register()

    with pytest.rasises(ValueError):

        # img_url is returns an HTTP status other than 200
        ot.user_profile_uploadphoto(token, img, x_start, y_start, x_end, y_end)

        # x_start, y_start, x_end, y_end 
        # are all within the dimensions of the image at the URL.
        ot.user_profile_uploadphoto(token, img, x_start, y_start, x_end, y_end)

def test_profile():

    token = account_register()
    invalid_u_id = 1234567

    with pytest.rasises(ValueError):

        # user with u_id is not a valid user
        ot.user_profile(token, invalid_u_id)