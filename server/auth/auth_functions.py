from json import dumps
from flask import Flask
import re
#import functions from another file

APP = Flask(__name__)

class Member:
    def __init__(self, u_id, name_first, name_last)
    

#self.handle = first + last;

data = {
    "messages": {} 
    "user_data": {}  
    "channel_id": {}
}

#in user_data:
#{u_id: {"email": email, "password": password, "name_first": name_first, "name_last": name_last, "handle": handle, "reset_code": reset_code, "token": token}, nextu_id, etc}

def get_user_data():
    global data
    return data.get("user_data")
    #return specific type of data?

#HELPER FUNCTIONS BELOW

def check_valid_email(email): 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        pass
    else:
        raise ValueError

def check_user_details(email, password, u_id):
    #fix this for new data representation!!
    u_data = get_user_data()
    
    if email in u_data:
        if u_data.get(email) == password:
            pass
        else:
            raise ValueError  
    else:
        raise ValueError
        
def check_valid_password(password):
    if len(password) < 6:
        raise ValueError
    else:
        pass
    
def check_email_already_exists(email):
    u_data = get_user_data()
    for u_id in u_data.keys:
        if u_data[u_id[email]] == email:
            raise ValueError


def check_name(name_first, name_last):
    if ((len(name_first) < 1) | (len(name_last) < 1)):
        raise ValueError
    else if ((len(name_first) > 50 | (len(name_last) > 50)):
        raise ValueError
    else:
        pass


#HELPER FUNCTIONS ABOVE

@APP.route("auth/login", methods=['POST'])
def auth_login():
    # fn_auth_login(request.args.get('email'), request.form.get('password'))
    #return dumps({})
    
    u_data = get_user_data()
    email = dumps((request.args.get('email'))
    password = dumps(request.args.get('password'))
    #get returns a dictionary ?
    check_valid_email(email)
    check_user_details(email, password)
    
    

@APP.route("auth/logout")
def auth_logout():
    pass
    
@APP.route("auth/register", methods =['POST'])
def auth_register():
    u_data = get_user_data()
    email = dumps((request.args.get('email'))
    password = dumps(request.args.get('password'))
    name_first = dumps(request.args.get('name_first'))
    name_last = dumps(request.args.get('name_last'))
    
    check_valid_email(email)
    check_valid_password(password)
    check_name(name_first, name_last)
    check_email_already_exists(email)
    
    u_id = len(u_data) + 1;
    
    
    
    
    return {u_id, token}


@APP.route("auth/passwordreset/request")
def auth_reset_request():
    pass

@APP.route("auth/passwordreset/reset")
def auth_reset():
    pass


if __name__ == "__main__":
    APP.run()
