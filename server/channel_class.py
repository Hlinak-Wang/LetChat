import uuid


class Channel:
    def __init__(self, channel_name, is_public, creator_id):
        self.channel_name = channel_name
        self.channel_id = uuid.uuid1().int
        self.owner_list = [creator_id]
        self.user_list = [creator_id]
        self.is_public = is_public
        self.standup = {'time_finish': 0, 'u_id': None}
        self.standup_message = ''

    def join_invite_channel(self, user):
        self.user_list.append(user)

    def leave_channel(self, user):
        self.user_list.remove(user)

    def add_owner(self, user_id):
        self.owner_list.append(user_id)

    def remove_owner(self, user_id):
        self.owner_list.remove(user_id)

    def get_channel_id(self):
        return self.channel_id

    def get_owner_list(self):
        return self.owner_list

    def get_user_list(self):
        return self.user_list

    def get_is_public(self):
        return self.is_public

    def get_channel_name(self):
        return self.channel_name

    def set_standup(self, time_finish, u_id):
        self.standup['time_finish'] = time_finish
        self.standup['u_id'] = u_id
