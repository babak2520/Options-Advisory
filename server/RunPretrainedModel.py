#!/usr/bin/env python
# coding: utf-8

# In[20]:


#this peice of code should run and return a dataframe if the neural network trained file and 
#historical data (at least for as many as the 'lookback' trading days) already exists
import pandas as pd
import numpy as np
from keras.models import load_model
from keras import backend as K


def predict_stock_price(df, desired_projection_date, trained_model_path, lookback):
    
    minimum, maximum = df['Close'].min(), df['Close'].max()

    df['Norm Actual Close'] = (df['Close'] - minimum) / (maximum - minimum)
    df['Norm Actual or Pred Close'] = df['Norm Actual Close'] 


    bd = pd.tseries.offsets.BusinessDay(n = 1)
    current_prediction_date = df.index[-1] + bd
    lstm_model = load_model(trained_model_path)
    while current_prediction_date <= desired_projection_date:
        model_input= df['Norm Actual or Pred Close'][-lookback-1 : -1].values
        model_input = model_input.reshape(1, model_input.shape[0], 1)
        prediction = lstm_model.predict(K.cast_to_floatx(model_input))
        df = df.append(pd.Series({'Norm Actual or Pred Close':prediction[0][0]
                                                  ,'Close':np.nan},name=current_prediction_date))
        current_prediction_date += bd

    df['Actual or Pred Close'] = minimum + df['Norm Actual or Pred Close'] * (maximum - minimum)
    del df['Norm Actual Close']
    del df['Norm Actual or Pred Close']
    return df



trained_model_path = 'trained models/EOG.h5'
lookback = 200
desired_projection_date = pd.Timestamp(year=2020, month=10, day=1)
historical_data_path = 'Data/EOG.csv'

df = pd.read_csv(historical_data_path, usecols = ['Date', 'Close'])
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace = True)



df = predict_stock_price(df, desired_projection_date, trained_model_path, lookback)

