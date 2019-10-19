from flask import Flask, request
from json import dumps

APP = Flask(__name__)


stack_channel = []
APP.route('/channel/create', methods=['POST'])
def channel_create():
    channel_name = request.form.get('channel_name')
    is_public = request.form.get('is_public')
    channel = Channel(channel_name, is_public)
    channel = channel.__dict__
    stack_channel.append(channel)
    return dumps(stack_channel)


APP.route('/channel/invite', methods=['POST'])
def channel_invite(channel_id, u_id):
    return dumps({})


@APP.route('channel/details', methods=['GET'])
def channel_details(token, channel_id):
    global data
    channelinformation = getData()