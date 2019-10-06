from Error import AccessError
import pytest

def auth_login(email, password):
    return u_id, token 

def auth_logout(token):
    return  

def auth_register(email, password, name_first, name_last):
    return u_id, token 

def auth_passwordreset_request(email):
    return 

def auth_passwordreset_reset(reset_code, new_password):
    return 

# Testing valid input for auth_login
def test_auth_login_ok():

    auth_key = auth_register("123456@gmail.com","123456789","W","S")

    return_key = auth_login("123456@gmail.com", "123456789")
    
    # Checking the output of auth_login is the same as auth_register
    assert return_key["token"] == auth_key["token"]
    assert return_key["u_id"] == auth_key["u_id"]
 

# Testing invalid input for auth_login
def test_auth_login_bad():

    auth_key = auth_register("123456@gmail.com","123456789","W","S")

    with pytest.raises(ValueError, match=r"*Invalid Email*"):
        auth_login("123456.gmail.com", "123456789")

    with pytest.raises(ValueError, match=r"*Email not registed*"):
        auth_login("123@gmail.com", "123456789")

    with pytest.raises(ValueError, match=r"*Wrong Password*"):
        auth_login("123456@gmail.com", "12345")


# Testing valid input for auth_logout
def test_auth_logout():

    auth_key = auth_register("123456@gmail.com","123456789","W","S")

    auth_logout(auth_key["token"])
    
    # if "token" is found in auth_key 
    # means the auth_logout is not working successfully
    if "token" in auth_key:
        logout = 0
    else:
        logout = 1
    
    assert logout == 1

# Testing valide input for auth_register
def test_auth_register_ok():

    auth_key = auth_register("123456@gmail.com","123456789","W","S")

    login = auth_login("123456@gmail.com","123456789")
    
    # Checking the user registered can login
    # And the output of auth_login is the same as auth_key
    assert login["token"] == auth_key["token"]
    assert login["u_id"] == auth_key["u_id"]

# Testing invalid input of auth_register
def test_auth_register_bad():
    
    with pytest.raises(ValueError, match=r"*Invalid Email*"):

        email = "ankitrai326.gmail.com"
        password = "123456789"
        name_first = "Yimeng"
        name_last = "Hu"

        auth_register(email, password, name_first, name_last)

    with pytest.raises(ValueError, match=r"*Invalid Password*"):
        email = "ankitrai326@gmail.com"
        password = "1234"
        name_first = "Yimeng"
        name_last = "Hu"

        auth_register(email, password, name_first, name_last)

    with pytest.raises(ValueError, match=r"*Invalid name_first*"):
        email = "ankitrai326@gmail.com"
        password = "123456789"
        name_first = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        name_last = "Hu"

        auth_register(email, password, name_first, name_last)

    with pytest.raises(ValueError, match=r"*Invalid name_last*"):
        email = "ankitrai326@gmail.com"
        password = "123456789"
        name_first = "Yimeng"
        name_last = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        auth_register(email, password, name_first, name_last)


# Testing valid input of auth_passwordreset_rest
def test_auth_passwordreset_reset_ok():

    auth_key = auth_register("ankitrai326@gmail.com","123456789","W","S")

    auth_passwordreset_request("ankitrai326@gmail.com")
    
    # Assume the reset_code obtained is 'asdf'
    reset_code = 'adsf'
    auth_passwordreset_reset(reset_code, "123456")
    
    # Using the new password to login
    # If the user is login successfully mean the password is successfully changed
    login = auth_login("ankitrai326@gmail.com","123456")
    assert login["token"] == auth_key["token"]
    assert login["u_id"] == auth_key["u_id"]

# Testing invalid input for auth_passwordreset_reset
def test_auth_passwordreset_reset_bad():

    auth_key = auth_register("ankitrai326@gmail.com","123456789","W","S")

    auth_passwordreset_request("ankitrai326@gmail.com")
    reset_code = 'adsf'
    
    with pytest.raises(ValueError, match=r"*Invalid reset code*"):
        auth_passwordreset_reset("8888", "123456")

    with pytest.raises(ValueError, match=r"*Invalid Password*"):
        auth_passwordreset_reset(reset_code, "1234")
