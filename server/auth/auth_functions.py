from json import dumps
from flask import Flask
import re
import jwt

#import functions from another file

APP = Flask(__name__)

class Member:
    def __init__(self, u_id, name_first, name_last)
    

#self.handle = first + last;

data = {
    "messages": {}, 
    "user_data": {},  
    "channel_id": {},
}

SECRET = 'IE4';

#in user_data:
#{u_id: {"email": email, "password": password, "name_first": name_first, "name_last": name_last, "handle": handle, "reset_code": reset_code, "token": token}, nextu_id, etc}

def get_user_data():
    global data
    global SECRET
    return data.get("user_data")
    #return specific type of data?

#HELPER FUNCTIONS BELOW

def check_valid_email(email): 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        pass
    else:
        raise ValueError

def check_user_details(email, password):
    #fix this for new data representation!!
    u_data = get_user_data()
    is_found = 0;
    for u_id, u_info in u_data.items():
        if u_info.get(email) == email:
            if u_info.get(password) == password:
                is_found = 1
                ID = u_id
                break
            else:
                raise ValueError  
    if is_found == 0:
        raise ValueError
    return ID
        
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
    email = request.args.get('email')
    password = request.args.get('password')
    #get returns a dictionary ?
    check_valid_email(email)
    u_id = check_user_details(email, password)
    
    token = jwt.encode({'password': password}, SECRET, algorithm = 'HS256')
    
    return dumps({u_id, token},
    })
    

@APP.route("auth/logout", methods = ['POST'])
def auth_logout():
    u_data = get_user_data()
    is_success = 1
    
    
    return dumps({is_sucess})
    
@APP.route("auth/register", methods =['POST'])
def auth_register():
    u_data = get_user_data()
    email = (request.args.get('email')
    password = request.args.get('password')
    name_first = request.args.get('name_first')
    name_last = request.args.get('name_last')
    
    check_valid_email(email)
    check_valid_password(password)
    check_name(name_first, name_last)
    check_email_already_exists(email)
    
    u_id = len(u_data) + 1;
    handle = generate_handle(name_first, name_last) # implement this
    token = jwt.encode({'password': password}, SECRET, algorithm = 'HS256')
    
    
    return {u_id, token}


@APP.route("auth/passwordreset/request")
def auth_reset_request():
    pass

@APP.route("auth/passwordreset/reset")
def auth_reset():
    pass


if __name__ == "__main__":
    APP.run()
