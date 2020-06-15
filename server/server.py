import os
from flask import Flask, render_template, request, url_for, jsonify, session
import json
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# create and configure the server
server = Flask(__name__)
server.config.from_mapping(
    SECRET_KEY='dev',
    SESSION_REFRESH_EACH_REQUEST=False,
    # TEMPLATES_AUTO_RELOAD=True,
    SESSION_TYPE='filesystem',
    CORS_HEADERS='Content-Type',
    TESTING=True
)

CORS(server)

async_mode = None
socketio = SocketIO(server, async_mode=async_mode, cors_allowed_origins="*")

try:
    os.makedirs(server.instance_path)
except OSError:
    print(OSError)
    pass

@server.route('/index')
def hello_flask():
    return ' YOLOOO!'

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('SEND_MESSAGE')
def client_send_message(data):
    print('client sent message!!!!!!!!!!!!!!!')
    print(data)
    print('emittingggggggggggggggggggggggggggggg')
    emit('update_on_layouts', {'data': 'Server generated event'})

if __name__ == ' __main__':
    socketio.run(host='0.0.0.0', debug=True, port=8050)
