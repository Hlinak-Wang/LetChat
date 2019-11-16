import hashlib
from datetime import datetime

class Data:

    def __init__(self):
        self.users_group = []
        self.channels_group = []
        self.messages_group = []

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def add_user(self, user):
        self.users_group.append(user)

    def add_channel(self, channel):
        self.channels_group.append(channel)

    def message_operation(self, message, action):
        if action == 'add':
            self.messages_group.insert(0, message)
        elif action == 'remove':
            self.messages_group.remove(message)

    def get_user_number(self):
        return len(self.users_group)

    def user_login_verify(self, email, password):
        for user in self.users_group:
            if user.email == email:
                if user.password == hashlib.sha256(password.encode("utf-8")).hexdigest():
                    return user
                else:
                    return {'ValueError': "Incorrect password entered"}
        return {'ValueError': "This email does not belong to a user"}

    def get_user(self, key, value):
        for user in self.users_group:
            if key == 'token':
                value_looking = user.token
            elif key == 'u_id':
                value_looking = user.u_id
            elif key == 'handle_str':
                value_looking = user.handle_str
            elif key == 'reset_code':
                value_looking = user.reset_code
            elif key == 'email':
                value_looking = user.email
            else:
                return None
            if value_looking == value:
                return user

        return None

    def get_channels_joined(self, u_id):
        channel_joined = []
        for channel in self.channels_group:
            if u_id in channel.user_list:
                channel_joined.append(channel.channel_id)
        return channel_joined

    def get_channel(self, channel_id):
        for channel in self.channels_group:
            if channel.channel_id == channel_id:
                return channel
        return None

    def get_message(self, message_id):
        for message in self.messages_group:
            if message.message_id == message_id:
                return message
        return None

    def check_unique(self, key, value):
        for user in self.users_group:
            if getattr(user, key) == value:
                return False
        return True

    def get_all_user_detail(self):
        all_user_detail = []
        for user in self.users_group:
            all_user_detail.append(user.get_user_detail())
        return all_user_detail

    def get_channel_list(self, u_id):
        channel_list = []
        for channel in self.channels_group:
            if u_id in channel.user_list:
                channel_list.append({
                    'name': channel.channel_name,
                    'channel_id': channel.channel_id
                })
        return {
            'channels': channel_list
        }

    def get_channel_list_all(self, u_id):
        channel_list_all = []
        for channel in self.channels_group:
            if channel.is_public or u_id in channel.user_list:
                channel_list_all.append({
                    'name': channel.channel_name,
                    'channel_id': channel.channel_id
                })

        return {
            'channels': channel_list_all
        }

    def get_channel_message(self, channel_id, u_id, start):
        channel_message = []
        counter = 0
        end = start
        time_now = datetime.now().timestamp()
        for message in self.messages_group[start:]:
            if message.channel_id == channel_id and message.time_created <= time_now:
                channel_message.append(message.get_message_info(u_id))
                counter += 1
            end += 1
            if counter >= 50:
                return {
                    'messages': channel_message,
                    'start': start,
                    'end': end
                }
        return {
            'messages': channel_message,
            'start': start,
            'end': -1
        }

    def get_earliest_index(self, channel_id):
        total_message = len(self.messages_group)
        for index in reversed(range(total_message)):
            message = self.messages_group[index]
            if message.channel_id == channel_id:
                return index
        return 0
