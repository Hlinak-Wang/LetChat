from flask import Flask
import re

APP = Flask(__name__)

class Member:
    def __init__(self, u_id, name_first, name_last)
    

#self.handle = first + last;

data = []

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check(email):  
        global regex
        if(re.search(regex,email)):  
            pass
        else:  
            raise ValueError

@APP.route("auth/login", methods=['POST'])
def auth_login():
    global data
    email = dumps((request.args.get('email'))
    password = dumps(request.args.get('password'))
    check(email)
    #get returns a dictionary ?
    

@APP.route("auth/logout")
def auth_logout():
    pass
    
@APP.route("auth/register")



@APP.route("auth/passwordreset/request")


@APP.route("auth/passwordreset/reset")



if __name__ == "__main__":
    APP.run()
