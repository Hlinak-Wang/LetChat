class data:
    def __int__(self):
        self.users = []
        self.channels = []
        self.message_counter = 0,
        self.message_buffer = []

    def user_create(self, name_first, name_last, email, password, token):
        new_user = User(name_first, name_last, email, password, token)
        self.users.append(new_user)

    def channel_create(self, channel_name):
        new_channel = Channel(channel_name)
        self.channels.append(new_channel)

    def get_user_all(self):
        return self.users

    def get_channel_all(self):
        return self.channels


class User:
    def __init__(self, name_first, name_last, email, password, token):
        self.name_first = name_first
        self.name_last = name_last
        self.email = email
        self.password = password
        self.token = token
        self.channel_involve = []
        self.u_id = 0
        self.handle_str = name_first + name_last
        self.reset_code = ''
        self.photo = 'https://bpic.588ku.com//element_origin_min_pic/19/01/04/46eb55e4401f9f4ddf449d1ba54b9871.jpg'

    def login(self, token):
        self.token = token

    def logout(self):
        self.token = None

    def reset_password(self, new_password):
        self.password = new_password

    def set_first_name(self, new_first):
        self.name_first = new_first

    def set_last_name(self, new_last):
        self.name_last = new_last

    def set_email(self, new_emil):
        self.email = new_emil

    def set_photo(self, new_photo):
        self.photo = new_photo

    def set_handle(self, new_handle):
        self.handle_str = new_handle

    def get_token(self):
        return self.token

    def get_uid(self):
        return self.u_id

    def get_handle(self):
        return self.handle_str

    def get_email(self):
        return self.email

    def get_photo(self):
        return self.photo

    def get_name_first(self):
        return self.name_first

    def get_name_last(self):
        return self.name_last


class Channel:
    def __init__(self, channel_name, is_public, creator_id):
        self.channel_name = channel_name
        self.channel_id = 0
        self.messages = []
        self.owner_list = [creator_id]
        self.user_list = [creator_id]
        self.is_public = is_public
        self.standup = {'time_finish': '1/1/1900, 1:00:00', 'u_id': None}
        self.standup_message = ''
        self.standup_queue = []

    def join_invite_channel(self, user):
        self.user_list.append(user)

    def leave_channel(self, user):
        self.user_list.remove(user)

    def add_owner(self, user_id):
        self.owner_list.append(user_id)

    def remove_owner(self, user_id):
        self.owner_list.remove(user_id)

    def send_message(self, content, channel_id, u_id, time_create):
        new_message = Message(content, channel_id, u_id, time_create)
        self.messages.append(new_message)

    def get_channel_id(self):
        return self.channel_id

    def get_owner_list(self):
        return self.owner_list

    def get_user_list(self):
        return self.user_list


class Message:
    def __init__(self, content, channel_id, u_id, time_create):
        self.channel_id = channel_id
        self.u_id = u_id,
        self.message_id = 0,
        self.message= content,
        self.time_created = time_create,
        self.reacts = [{'react_id': 1, 'u_ids': []}],
        self.is_pinned = False


