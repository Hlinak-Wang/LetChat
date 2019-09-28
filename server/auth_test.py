def auth_login(email, password):
    return token 

def auth_logout(token):
    return token 

def auth_register(email, password, name_first, name_last):
    return token 

def auth_passwordreset_request(email):
    return 

def auth_passwordreset_reset(reset_code, new_password):
    return token 



import auth_login
import auth_logout
import auth_register
import auth_passwordreset_request
import auth_passwordreset_reset

      
def test_auth_login():

    token = auth_register("123456@gmail.com","123456789","W","S")

    assert auth_login("123456.gmail.com", "123456789") = "Invalid Email"

    assert auth_login("123@gmail.com", "123456789") = "Email not registed"

    assert auth_login("123456.gmail.com", "12345") = "Wrong Password"

    auth_login("123456@gmail.com", "123456789") = token
    assert type(token) = str



def test_auth_logout():

    auth_login(123456@gmail.com, 123456789) = token

    token_logout = auth_logout(token):
    assert type(token_logout) = str



def test_auth_register():
 
    email = "ankitrai326.gmail.com"
    password = "123456789"
    name_first = "Yimeng"
    name_last = "Hu"

    assert auth_register(email, password, name_first, name_last) = "Invalid Email"

    email = "ankitrai326@gmail.com"
    password = "1234"
    name_first = "Yimeng"
    name_last = "Hu"

    assert auth_register(email, password, name_first, name_last) = "Invalid Password"

    email = "ankitrai326@gmail.com"
    password = "123456789"
    name_first = "012345678901234567890123456789012345678901234567890123456789"
    name_last = "Hu"

    assert auth_register(email, password, name_first, name_last) = "Invalid name_first"

    email = "ankitrai326@gmail.com"
    password = "123456789"
    name_first = "Yimeng"
    name_last = "012345678901234567890123456789012345678901234567890123456789"

    assert auth_register(email, password, name_first, name_last) = "Invalid name_last"

    email = "ankitrai326@gmail.com"
    password = "123456789"
    name_first = "Yimeng"
    name_last = "Hu"

    assert auth_register(email, password, name_first, name_last) = token


def test_auth_passwordreset_request():
 
    code = auth_passwordreset_request(ankitrai326@gmail.com)
    assert type(code) = str

def test_auth_passwordreset_reset():

    assert auth_passwordreset_request(ankitrai326@gmail.com) = "Invalid email"

    reset_code = auth_passwordreset_request(ankitrai326@gmail.com)

    assert auth_passwordreset_reset("8888", "123456") = "Invalid reset_code"

    assert auth_passwordreset_reset(reset_code, "123456") = "Invalid Password"
