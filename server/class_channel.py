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