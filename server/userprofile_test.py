import pytest

def auth_register(email, password, first_nanme, last_name):
	
    pass

def channels_create(token, name, is_public):
	pass

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

    # create one user
    auth_key = auth_register('123@gmail.com', '123412', 'HHH', 'LLLL')

    #name_first more than 50 characters but not name_last
    first_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    first_short = 'asdfzxcv'

    last_short = 'abcd'
    last_long = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    # Invalid input 
    with pytest.rasises(ValueError, match=r".*name_first is more than 50 characters.*"):

        user_profile_setname(auth_key["token"],first_long,last_short)

    with pytest.rasises(ValueError, match=r".*name_last is more than 50 characters.*"):

        user_profile_setname(auth_key["token"], first_short, last_long)

    # Valid input
    user_profile_setname(auth_key["token"], first_short, last_short)
    profile = user_profile(auth_key["token"], auth_key["u_id"])
    assert profile["name_first"] == first_short
    assert profile["name_last"] == last_short
    
def test_setemail():
    
    # Register two user for testing
    auth_key = auth_register('123@gmail.com', '123412', 'HHH', 'LLLL')
    auth_key2 = auth_register('adfzcv@gmail.com', '12341212', 'HHH', 'LLLL')
    
    invalid_email = 'dffgfddfsa.com'
    email_used_already = 'adfzcv@gmail.com'
    
    # Invalid input
    with pytest.rasises(ValueError, match=r".*Email entered is not a valid email.*"):

        user_profile_setemail(auth_key["token"],invalid_email)

    with pytest.rasises(ValueError, match=r".*Email address is already being used by another user.*"):

        user_profile_setemail(auth_key["token"],email_used_already)
    
    # Valid input
    user_profile_setemail(auth_key["token"], 'newemail@gmail.com')
    profile = user_profile(auth_key["token"], auth_key["u_id"])
    assert profile["email"] == 'newemail@gmail.com'

def test_sethandle():

    auth_key = auth_register('123@gmail.com', '123412', 'HHH', 'LLLL')
    
    handle_long = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' 
    
    # Invalid input
    with pytest.rasises(ValueError, match=r".*handle_str is no more than 20 characters.*"):

        # handle_str is no more than 20 charaters
        user_profile_sethandle(auth_key["token"], handle_long)
    
    # Valid input
    user_profile_sethandle(auth_key["token"], 'testing')
    profile = user_profile(auth_key["token"], auth_key["u_id"])
    assert profile["handle_str"] == 'testing'
    
def test_uploadphoto():

    # Create one user for testing
    auth_key = auth_register('123@gmail.com', '123412', 'HHH', 'LLLL')
    img_notURL = 'asdfzxvzdsaewrasdf'
    
    x_start_in = 0
    y_start_in = 0
    x_end_in = 100
    y_end_in = 100
    
    with pytest.rasises(ValueError, match=r".*img_url is returns an HTTP status other than 200.*"):

        user_profile_uploadphoto(auth_key["token"], img_notURL, x_start_in, y_start_in, x_end_in, y_end_in)
    
    img_URL = 'https://unsplash.com/photos/8IY27TsGaVE'
    x_start_out = -19
    y_start_out = -10
    x_end_out = 1111111111111111111111111111111111111111111111111
    y_end_out = 1111111111111111111111111111111111111111111111111
    
    with pytest.rasises(ValueError, match=r".*x_start, y_start, x_end, y_end are all within the dimensions of the image at the URL.*"):
        
        user_profile_uploadphoto(auth_key["token"], img_URL, x_start_out, y_start_in, x_end_in, y_end_in)
        
        user_profile_uploadphoto(auth_key["token"], img_URL, x_start_in, y_start_out, x_end_in, y_end_in)
        
        user_profile_uploadphoto(auth_key["token"], img_URL, x_start_in, y_start_in, x_end_out, y_end_in)
        
        user_profile_uploadphoto(auth_key["token"], img_URL, x_start_in, y_start_in, x_end_in, y_end_out)
        
        user_profile_uploadphoto(auth_key["token"], img_URL, x_start_out, y_start_out, x_end_out, y_end_out)
        
    
def test_profile():
    
    # Create one user for testing
    auth_key = auth_register('123@gmail.com', '123412', 'HHH', 'LLLL')
    invalid_u_id = auth_key["token"] + 1234562345462134546
    
    # Invalid input
    with pytest.rasises(ValueError, match=r".*User with u_id is not a valid user.*"):
        user_profile(auth_key["token"], invalid_u_id)
        
    # Valid input
    return_key = user_profile(auth_key["token"], auth_key["u_id"])
    assert return_key["email"] == '123@gmail.com'
    assert return_key["name_first"] == 'HHH'
    assert return_key["name_last"] == 'LLLL'
    # Assume the default handle is the first_namelast_name
    assert return_key["handle_str"] == 'HHHLLLL'
