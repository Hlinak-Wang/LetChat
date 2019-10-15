from json import dumps
from flask import Flask
import re
#import functions from another file

APP = Flask(__name__)

class Member:
    def __init__(self, u_id, name_first, name_last)
    

#self.handle = first + last;

data = {
    

}

def getData():
    global data
    return data

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check_valid_email(email):  
        global regex
        if(re.search(regex,email)):  
            pass
        else:
            raise ValueError
def check_user_email(email):
    data = getData()
    

@APP.route("auth/login", methods=['POST'])
def auth_login():
    # fn_auth_login(request.args.get('email'), request.form.get('password'))
    #return dumps({})
    
    data = getData()
    email = dumps((request.args.get('email'))
    password = dumps(request.args.get('password'))
    #get returns a dictionary ?
    check_valid_email(email)
    check_user_email(email)
    check_user_password(password)
    
    

@APP.route("auth/logout")
def auth_logout():
    pass
    
@APP.route("auth/register")



@APP.route("auth/passwordreset/request")


@APP.route("auth/passwordreset/reset")



if __name__ == "__main__":
    APP.run()
