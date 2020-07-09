from server.RunPretrainedModel import predict_stock_price
import os
from flask import Flask, render_template, request, url_for, jsonify, session
import json
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pandas as pd

# create and configure the server
server = Flask(__name__)
server.config.from_mapping(
    SECRET_KEY='dev',
    SESSION_REFRESH_EACH_REQUEST=False,
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
    return ' Hello Flask!'


@socketio.on('SEND_MESSAGE')
def client_send_message(data):
    print('client sent message to the server!')
    socketio.emit('message_to_client', {'data': 'you received this message from the server'})


@socketio.on('ping')
def pongResponse():
    socketio.emit('pong')


@socketio.on('client_gives_form_data')
def get_form_data(d):
    data = d['data']
    projection_date = pd.to_datetime(data['desired_projection_date'], infer_datetime_format=True,
                                     errors='coerce',
                                     format='%Y-%m-%d %H:%M:%S')
    lookback = int(data['lookback'])
    stock = data['stock']

    print("here is the passed data")
    print(projection_date, lookback, stock)
    ##ToDo do some calculation pass the result to the client
    trained_model_path = 'trained models/EOG.h5'

    historical_data_path = 'Data/EOG.csv'

    df = pd.read_csv(historical_data_path, usecols=['Date', 'Close'])
    #df['Date'] = pd.to_datetime(df['Date'])
    #df.set_index('Date', inplace=True)

    df = predict_stock_price(df, projection_date, trained_model_path, lookback)
    socketio.emit('plot_data_from_server', {'data': df.to_json()})
    print('tried emitting following data: {}'.format(df))



        # jsonfiles = json.loads(json.dumps(dict_to_update))
        # return jsonify(jsonfiles)

#def emit_plot_data():
#    data = 123  # preparing the data in dictionary format maybe needed to convert to json, I dont know yet.
#    socketio.emit('plot_data_from_server', data)


if __name__ == ' __main__':
    socketio.run(host='0.0.0.0', debug=True, port=8050)
