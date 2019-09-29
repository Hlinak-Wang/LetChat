import pytest

def auth_register(email, password, first_nanme, last_name):
	
	u_id = 123
	token = 355
	return u_id, token

def channels_create(token, name, is_public):
	channel_id = 12345
	return channel_id

def user_profile_setname(token, first_long, last_short):
    pass

def user_profile_setemail(token, email):
    pass

def user_profile_sethandle(token, handle_str):
    pass

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    pass

def user_profile(token, u_id):
    
    #return email, name_first, name_last, handle_str
    pass

def test_setname():

    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')

    #name_first more than 50 characters but not name_last
    first_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    first_short = 'asdfzxcv'

    last_short = 'abcd'
    last_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    # Invalid input 
    with pytest.rasises(ValueError, match=r".*name_first is more than 50 characters.*"):

        user_profile_setname(token,first_long,last_short)

    with pytest.rasises(ValueError, match=r".*name_last is more than 50 characters.*"):

        user_profile_setname(token, first_short, last_long)

    # Valid input
    user_profile_setname(token, first_short, last_short)
    email, name_first, name_last, handle_str = user_profile(token, u_id)
    assert name_first == first_short
    assert name_last == last_short
    
def test_setemail():

    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    
    token_other, u_id_other = auth_register('adfzcv@gmail.com', 123412, 'HHH', 'LLLL')
    
    invalid_email = 'dffgfddfsa.com'
    email_used_already = 'adfzcv@gmail.com'
    
    # Invalid input
    with pytest.rasises(ValueError, match=r".*Email entered is not a valid email.*"):

        user_profile_setemail(token,invalid_email)

    with pytest.rasises(ValueError, match=r".*Email address is already being used by another user.*"):

        user_profile_setemail(token,email_used_already)
    
    # Valid input
    user_profile_setemail(token, 'newemail@gmail.com')
    email, name_first, name_last, handle_str = user_profile(token, u_id)
    assert email == 'newemail@gmail.com'

def test_sethandle():

    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    
    handle_long = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' 
    
    # Invalid input
    with pytest.rasises(ValueError, match=r".*handle_str is no more than 20 characters.*"):

        # handle_str is no more than 20 charaters
        user_profile_sethandle(token, handle_long)
    
    # Valid input
    user_profile_sethandle(token, 'testing')
    email, name_first, name_last, handle_str = user_profile(token, u_id)
    assert handle_str == 'testing'
    
def test_uploadphoto():

    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    img_notURL = 'asdfzxvzdsaewrasdf'
    
    x_start_in = 0
    y_start_in = 0
    x_end_in = 100
    y_end_in = 100
    
    with pytest.rasises(ValueError, match=r".*img_url is returns an HTTP status other than 200.*"):

        user_profile_uploadphoto(token, img_notURL, x_start_in, y_start_in, x_end_in, y_end_in)
    
    img_URL = 'https://unsplash.com/photos/8IY27TsGaVE'
    x_start_out = -19
    y_start_out = -10
    x_end_out = 1111111111111111111111111111111111111111111111111
    y_end_out = 1111111111111111111111111111111111111111111111111
    
    with pytest.rasises(ValueError, match=r".*x_start, y_start, x_end, y_end are all within the dimensions of the image at the URL.*"):
        
        user_profile_uploadphoto(token, img_URL, x_start_out, y_start_in, x_end_in, y_end_in)
        
        user_profile_uploadphoto(token, img_URL, x_start_in, y_start_out, x_end_in, y_end_in)
        
        user_profile_uploadphoto(token, img_URL, x_start_in, y_start_in, x_end_out, y_end_in)
        
        user_profile_uploadphoto(token, img_URL, x_start_in, y_start_in, x_end_in, y_end_out)
        
        user_profile_uploadphoto(token, img_URL, x_start_out, y_start_out, x_end_out, y_end_out)

def test_profile():

    token, u_id = auth_register('123@gmail.com', 123412, 'HHH', 'LLLL')
    invalid_u_id = 1234567
    
    # Invalid input
    with pytest.rasises(ValueError, match=r".*User with u_id is not a valid user.*"):
        user_profile(token, invalid_u_id)
        
    # Valid input
    email, name_first, name_last, handle_str = user_profile(token, u_id)
    assert email == '123@gmail.com'
    assert name_first == 'HHH'
    assert name_last == 'LLLL'
    # Assume the default handle is the last_name
    assert handle_str == 'LLLL'