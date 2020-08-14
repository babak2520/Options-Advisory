from server.StockModules import stockDataPrep, stockLSTM, updateStockData, updateNetworks, \
    loadNNFromFile, updatePredictions, optionStrategy
import os
from flask import Flask, render_template, request, url_for, jsonify, session
import json
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pandas as pd
from pathlib import Path
from pandas_datareader import data as web
from datetime import date
import time

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
################################ Core script
AllStocks = ['XOM', 'CVX', 'COP', 'HAL', 'SLB', 'GE', 'GOOG', 'NFLX', 'C', 'DAL', 'AMZN', 'V']
LoadfromFile = False ##ToDo this flag (if false) will retrain neural networks and save and load a new set of files.
BDProjection = pd.tseries.offsets.BusinessDay(800)
NNUpdateInt = 5

if not LoadfromFile:
    CloseNNDict = updateNetworks(AllStocks, response='Close_grad', BDinterval = 3)
    VolatilityNNDict = updateNetworks(AllStocks, response='Volatility', BDinterval = 3)
else:
    CloseNNDict = loadNNFromFile(AllStocks, response='Close_grad')
    VolatilityNNDict = loadNNFromFile(AllStocks, response='Volatility')

ClosePredictionsDict, VolatilityPredictionsDict = {} , {}
Counter = 0

while True:
    ClosePredictionsDict = updatePredictions(AllStocks, CloseNNDict, pd.to_datetime('today')+BDProjection, response = 'Close_grad')
    VolatilityPredictionsDict = updatePredictions(AllStocks, VolatilityNNDict, pd.to_datetime('today')+BDProjection, response = 'Volatility')
    time.sleep(60*60*24)
    Counter+=1
    if Counter == NNUpdateInt:
        CloseNNDict = updateNetworks(AllStocks, response='Close')
        VolatilityNNDict = updateNetworks(AllStocks, response='Volatility')
        Counter = 0
##############################

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

    socketio.emit('plot_data_from_server', {'data': ClosePredictionsDict['SLB'].to_json(orient='index')})




if __name__ == ' __main__':
    socketio.run(host='0.0.0.0', debug=True, port=8050)
