import uuid


class Message:
    def __init__(self, content, channel_id, u_id, time_create):
        self._channel_id = channel_id
        self._u_id = u_id
        self._message_id = uuid.uuid1().int
        self.message = content
        self.time_created = time_create,
        self.reacts = [React(1)]
        self.is_pinned = False

    def get_message_id(self):
        return self._message_id

    def get_channel_id(self):
        return self._channel_id

    def get_content(self):
        return self.message

    def user_get_sender_id(self):
        return self._u_id

    def get_pin_state(self):
        return self.is_pinned

    def user_edit(self, new_content):
        self.message = new_content

    def user_pin(self):
        self.is_pinned = True

    def user_unpin(self):
        self.is_pinned = False

    def get_react_by_id(self, react_id):
        for react in self.reacts:
            if react.get_react_id() == react_id:
                return react
        return None

    def __get_react_all(self, u_id):
        react_list = []
        for react in self.reacts:
            react_list.append(react.get_react_detail(u_id))
        return react_list

    def get_message_info(self, u_id):

        message_info = {
            'message_id': self._message_id,
            'u_id': self._u_id,
            'message': self.message,
            'time_created': self.time_created,
            'reacts': self.__get_react_all(u_id)
        }
        return message_info


class React:
    def __init__(self, react_id):
        self.react_id = react_id
        self.u_ids = []

    def user_react(self, u_id):
        self.u_ids.append(u_id)

    def user_unreact(self, u_id):
        self.u_ids.remove(u_id)

    def get_react_id(self):
        return self.react_id

    def get_u_ids(self):
        return self.u_ids

    def is_react(self, u_id):
        if u_id in self.u_ids:
            return True
        else:
            return False

    def get_react_detail(self, u_id):
        return {
            'react_id': self.react_id,
            'u_ids': self.u_ids,
            'is_this_user_reacted': self.is_react(u_id)
        }
