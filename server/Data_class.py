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

    def get_element(self, aspect, key, value):
        aspect_looking = getattr(self, aspect)
        for element in aspect_looking:
            if getattr(element, key) == value:
                return element

        return None

    def check_unique(self, aspect, key, value):
        aspect_looking = getattr(self, aspect)
        for element in aspect_looking:
            if getattr(element, key) == value:
                return False
        return True

    def get_channels_joined(self, u_id):
        channel_joined = []
        for channel in self.channels_group:
            if u_id in channel.user_list:
                channel_joined.append(channel.channel_id)
        return channel_joined

    def get_all_user_detail(self, host):
        all_user_detail = []
        for user in self.users_group:
            all_user_detail.append(user.get_user_detail('individual', host))
        return all_user_detail

    def get_earliest_index(self, channel_id):
        total_message = len(self.messages_group)
        for index in reversed(range(total_message)):
            message = self.messages_group[index]
            if message.channel_id == channel_id:
                return index
        return 0
