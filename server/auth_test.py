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

      
def test_auth_login_ok():

    auth_key = auth_register("123456@gmail.com","123456789","W","S")

    return_key = auth_login("123456@gmail.com", "123456789")

    assert return_key["token"] == auth_key["token"]
    assert return_key["u_id"] == auth_key["u_id"]
 

def test_auth_login_bad():
    #ValueError

    auth_key = auth_register("123456@gmail.com","123456789","W","S")

    with pytest.raises(ValueError, match=r"*Invalid Email*"):
        auth_login("123456.gmail.com", "123456789")

    with pytest.raises(ValueError, match=r"*Email not registed*"):
        auth_login("123@gmail.com", "123456789")

    with pytest.raises(ValueError, match=r"*Wrong Password*"):
        auth_login("123456@gmail.com", "12345")



def test_auth_logout():

    auth_key = auth_register("123456@gmail.com","123456789","W","S")

    auth_logout(auth_key["token"])

    if "token" in auth_key:
        logout = 0
    else:
        logout = 1
    
    assert logout == 1

def test_auth_register_ok():

    auth_key = auth_register("123456@gmail.com","123456789","W","S")

    login = auth_login("123456@gmail.com","123456789")
    assert login["token"] == auth_key["token"]
    assert login["u_id"] == auth_key["u_id"]

def test_auth_register_bad():
    #ValueError
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

def test_auth_passwordreset_request():
 
    code = auth_passwordreset_request("ankitrai326@gmail.com")
    assert type(code) == str


def test_auth_passwordreset_reset_ok():

    auth_key = auth_register("ankitrai326@gmail.com","123456789","W","S")

    auth_passwordreset_request("ankitrai326@gmail.com")

    reset_code = 'adsf'
    auth_passwordreset_reset(reset_code, "123456")
    login = auth_login("ankitrai326@gmail.com","123456")
    assert login["token"] == auth_key["token"]
    assert login["u_id"] == auth_key["u_id"]


def test_auth_passwordreset_reset_bad():
    #ValueError
    auth_key = auth_register("ankitrai326@gmail.com","123456789","W","S")

    auth_passwordreset_request("ankitrai326@gmail.com")
    reset_code = 'adsf'
    
    with pytest.raises(ValueError, match=r"*Invalid reset code*"):
        auth_passwordreset_reset("8888", "123456")

    with pytest.raises(ValueError, match=r"*Invalid Password*"):
        auth_passwordreset_reset(reset_code, "1234")
