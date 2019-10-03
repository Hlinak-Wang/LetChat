from Error import AccessError

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



import auth_login
import auth_logout
import auth_register
import auth_passwordreset_request
import auth_passwordreset_reset

      
def test_auth_login_ok():

    {u_id, token} = auth_register("123456@gmail.com","123456789","W","S")

    assert auth_login("123456@gmail.com", "123456789") = {u_id, token}


def test_auth_login_bad():
    #ValueError
    {u_id, token} = auth_register("123456@gmail.com","123456789","W","S")

    with pytest.raises(ValueError, match=r"*Invalid Email*"):
        auth_login("123456.gmail.com", "123456789")

    with pytest.raises(ValueError, match=r"*Email not registed*"):
        auth_login("123@gmail.com", "123456789")

    with pytest.raises(ValueError, match=r"*Wrong Password*"):
        auth_login("123456.gmail.com", "12345")



def test_auth_logout():

    auth_login(123456@gmail.com, 123456789) = token

    assert type(token) = str

    token_logout = auth_logout(token):



def test_auth_register_ok():

    email = "ankitrai326@gmail.com"
    password = "123456789"
    name_first = "Yimeng"
    name_last = "Hu"

    assert auth_register(email, password, name_first, name_last) = token

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

        auth_register(email, password, name_first, name_last) = ""

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
 
    code = auth_passwordreset_request(ankitrai326@gmail.com)
    assert type(code) = str


def test_auth_passwordreset_reset_ok():

    reset_code = auth_passwordreset_request(ankitrai326@gmail.com)

    auth_passwordreset_reset(reset_code, "123456")


def test_auth_passwordreset_reset_bad():
    #ValueError

    reset_code = auth_passwordreset_request(ankitrai326@gmail.com)

    with pytest.raises(ValueError, match=r"*Invalid reset code*"):
        auth_passwordreset_reset("8888", "123456")

    with pytest.raises(ValueError, match=r"*Invalid Password*"):
        auth_passwordreset_reset(reset_code, "1234")
 