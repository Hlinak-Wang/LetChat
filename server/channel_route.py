from flask import Flask, request
from json import dumps
from channel_function import ch_create, ch_invite,ch_details
APP = Flask(__name__)

APP.route('channel/create', methods=['POST'])
def channel_create():
    channel_id = ch_create()
    return dumps({channel_id})

APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    ch_invite()
    return dumps({})

@APP.route('channel/details', methods=['GET'])
def channel_details(token, channel_id):
    detail = ch_details()
    return dumps({detail})

@APP.route('channel/message', methods=['GET'])
def cahnnel_message():

    return dumps({})
