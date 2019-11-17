import uuid
from flask import request


class User:
    def __init__(self, name_first, name_last, email, password, handle, token, permission_id, host):
        self.name_first = name_first
        self.name_last = name_last
        self.email = email
        self.permission_id = permission_id
        self.password = password
        self.token = token
        self.u_id = int(uuid.uuid1().int / (10**25))
        self.handle_str = handle
        self.reset_code = ''
        self.profile_img_url = host + 'static/default.jpg'

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def login(self, token):
        self.token = token

    def logout(self):
        self.token = None

    def password_code(self, code):
        self.reset_code = code

    def reset_password(self, new_password):
        self.password = new_password
        self.reset_code = ''

    def set_first_name(self, new_first):
        self.name_first = new_first

    def set_last_name(self, new_last):
        self.name_last = new_last

    def set_email(self, new_emil):
        self.email = new_emil

    def set_photo(self, new_photo):
        self.profile_img_url = new_photo

    def set_handle(self, new_handle):
        self.handle_str = new_handle

    def set_permission_id(self, new_permission):
        self.permission_id = new_permission

    def get_user_detail(self, action, host):

        if self.profile_img_url.find('default.jpg') == -1:
            self.profile_img_url = host + 'static/' + str(self.u_id) + '.jpg'
        else:
            self.profile_img_url = host + 'static/default.jpg'

        user_detail = {}
        if action == 'individual':
            user_detail = {
                'u_id': self.u_id,
                'email': self.email,
                'name_first': self.name_first,
                'name_last': self.name_last,
                'handle_str': self.handle_str,
                'profile_img_url': self.profile_img_url
            }
        elif action == 'member':
            user_detail = {
                'u_id': self.u_id,
                'name_first': self.name_first,
                'name_last': self.name_last,
                'profile_img_url': self.profile_img_url
            }

        return user_detail

