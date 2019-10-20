from flask import Flask, request
from json import dumps
from channel_function import ch_create, ch_invite,ch_details, ch_leave, ch_join, ch_addowner, ch_removeowner, ch_lists, ch_listall, ch_me
APP = Flask(__name__)

APP.route('/channels/create', methods=['POST'])
def channel_create():
    channel_id = ch_create()
    return dumps({channel_id})

APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    ch_invite()
    return dumps({})

@APP.route('/channel/details', methods=['GET'])
def channel_details(token, channel_id):
    detail = ch_details()
    return dumps({detail})

@APP.route('/channel/message', methods=['GET'])
def channel_message():

    return dumps({})

@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    ch_leave()
    return dumps({})
    
@APP.route('/channel/join', methods=['POST'])
def channel_join():
    ch_join()
    return dumps({})
@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    ch_addowner()
    return dumps({})
    
@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    ch_removeowner()
    return dumps({})
    
@APP.route('/channels/list', methods=['GET'])
def channel_list():
    lists = ch_lists
    return dumps({lists})
    
@APP.route('/channels/listall', methods=['GET'])
def channel_listall():
    listall = ch_listall()
    return dumps({listall})
