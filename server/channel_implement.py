from flask import Flask, request
from json import dumps

APP = Flask(__name__)

class Channel:
    def __init__(self, name, is_public):
        self.name = name
        self.is_public = is_public

stack_channel = []
@APP.route('/channel/create', methods=['POST'])
def channel_create():
    channel_name = request.form.get('channel_name')
    is_public = request.form.get('is_public')
    channel = Channel(channel_name, is_public)
    channel = channel.__dict__
    stack_channel.append(channel)
    return dumps(stack_channel)

if __name__ == '__main__':
    APP.run(debug=True)