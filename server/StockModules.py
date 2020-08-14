import pandas as pd
import numpy as np
import random
##imports needed for stockLSTM class
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
import matplotlib.pyplot as plt
import json
import os
from pathlib import Path
from keras.models import load_model
from pandas_datareader import data as web



class stockDataPrep:
    def __init__(self, HistoricalData=None):
        if HistoricalData is not None:
            if type(HistoricalData) != pd.core.frame.DataFrame:
                raise Exception("Only pandas dataframes are allowed as stockPricePredicor class data.")
            elif type(HistoricalData.index) != pd.core.indexes.datetimes.DatetimeIndex:
                raise Exception("Pandas dataframe should have a pandas.core.indexes.datetimes.Datetime Index.")
            else:
                self.__masterdata = HistoricalData
                self.__masterdata = self.__masterdata.sort_index(ascending=True, axis=0)

    def reprocessData(self, BDinterval, createVolatilityFeature=True, gradientFeatures=[]):
        # create a uniformly sampled dataset by the frequency of number of business days BDinterval
        timeoffset = pd.tseries.offsets.BusinessDay(BDinterval)
        resampled_dataset = self.__masterdata.copy()
        if createVolatilityFeature:
            resampled_dataset['Volatility'] = 2 * (resampled_dataset['High'] - resampled_dataset['Low']) / (
                    resampled_dataset['High'] + resampled_dataset['Low'])
            resampled_dataset['Volatility'] = np.log(resampled_dataset['Volatility'])
        resampled_dataset = resampled_dataset.resample(timeoffset).mean()
        for feature in gradientFeatures:
            gradf = feature + '_grad'
            resampled_dataset[gradf] = None
            gradfloc = resampled_dataset.columns.get_loc(gradf)
            floc = resampled_dataset.columns.get_loc(feature)
            for i in range(1, len(resampled_dataset)):
                resampled_dataset.iat[i, gradfloc] = (
                        (resampled_dataset.iloc[i, floc] - resampled_dataset.iloc[i - 1, floc]) /
                        resampled_dataset.iloc[i - 1, floc])
            resampled_dataset.fillna(method='bfill', inplace=True)
            resampled_dataset.fillna(method='ffill', inplace=True)

        # if resampled_dataset.index[-1] > self.__masterdata.index[-1]:
        #     print("dropping last row timestamp {} in {} resampled dataset because it appears to be an extrapolation to the last\
        #     real date available at {}".format(resampled_dataset.index[-1], freq, self.__masterdata.index[-1]))
        #     resampled_dataset.drop(resampled_dataset.index[-1], inplace=True)
        return resampled_dataset

    def createFeedData(self, BDinterval, lookback, projectforward=1, features=None,
                       response=['Close_grad']):
        # Create the feed x and y data for LSTM based on lookback and the features to be included in lookback,
        # and the number of timesteps to project (project forward). This method uses the private class member __masterdata
        if features is None:
            features = self.__masterdata.columns
        gradfeatures = [entry[:-5] for entry in features if entry.endswith("_grad")]
        dataset = self.reprocessData(BDinterval, gradientFeatures=gradfeatures)

        if len(response) > 1:
            raise Exception(
                "Multiple response (y) features are not currently supported. Train separate networks for each response.")

        x_train_data, y_train_data = [], []

        # scale x and y data using a simple min and max scaler
        x_scaled_data = np.transpose(dataset[features].to_numpy())
        for entry in x_scaled_data:
            maximum = entry.max()
            minimum = entry.min()
            entry[:] = (entry[:] - minimum) / (maximum - minimum)

        y_scaled_data = np.transpose(dataset[response[:]].to_numpy())
        for entry in y_scaled_data:
            maximum = entry.max()
            minimum = entry.min()
            entry[:] = (entry[:] - minimum) / (maximum - minimum)
        x_scaled_data, y_scaled_data = np.transpose(x_scaled_data), np.transpose(y_scaled_data)

        # initialize x and y data into proper shape (total data points to fed, timesteps in each datapoint, number of features)
        x_train_data = np.ndarray(shape=(len(x_scaled_data) - lookback - projectforward + 1, lookback, len(features)))
        y_train_data = np.ndarray(
            shape=(len(y_scaled_data) - lookback - projectforward + 1, projectforward, len(response)))

        # construct the x and y data to be fed from the original scaled sets
        for i in range(x_train_data.shape[0]):
            x_train_data[i, :, :] = x_scaled_data[i:i + lookback, :]
            y_train_data[i, :, :] = y_scaled_data[i + lookback:i + lookback + projectforward, :]
        return (x_train_data, y_train_data, dataset.describe())

    def test_train_split(self, data, traintotalratio=0.75, how='testend', order='preserved'):
        # method to take a tuple of properly formated feed data (the format coming out of createFeedData method) and split
        # the data into two sets of test and train. The "how" indicates where are the test data selected, for example,
        # "testend" selects the test data from the very end of the dataset and "random" selects the test data randomly.
        # the "order" indicated whether the order of the data in the test and train subsets will be in the same order as the
        # original set of to be randomized.
        lenset = set({})
        for entry in data:
            lenset.add(len(entry))
        if len(lenset) != 1:
            raise Exception("data should be a list or tuple of datasets of equal lengths")

        length = lenset.pop()

        if how == 'random':
            trainset = random.sample(range(length), int(length * traintotalratio))
        elif how == 'testbeginning':
            trainset = list(range(int(length * (1 - traintotalratio)), length))
        elif how == 'testmiddle':
            trainset = list(range(int(length * traintotalratio / 2))) + list(
                range(int(length * (2 - traintotalratio) / 2), length))
        elif how == 'testend':
            trainset = list(range(int(length * traintotalratio)))
        else:
            raise Exception("no implementation for how = {}".format(how))

        testset = list(set(range(length)).difference(trainset))

        if order == 'randomized':
            random.shuffle(trainset)
            random.shuffle(testset)
        elif order == 'preserved':
            trainset.sort()
            testset.sort()
        else:
            raise Exception("no implementation for order = {}".format(order))

        output = []
        for entry in data:
            output.append([entry[testset, :, :], entry[trainset, :, :]])
        return output

########################################################


class stockLSTM:

    def __init__(self, lookback=None, projectforward=None, features=None, loadfromfile=False,
                 filestemname=None, folder='trained models', underlying=None, response=None):

        if loadfromfile:
            if filestemname == None:
                raise Exception('filestemname variable should be supplied if loadfromfile is true')
            else:
                self.loadRegressor(filestemname, folder)
        else:
            if lookback == None or projectforward == None or features == None:
                raise Exception(
                    'lookback, projectforward, and features variables should be supplied if loadfromfile is false')
            else:
                self.lookback = lookback
                self.projectforward = projectforward
                self.features = features
                self.underlying = underlying
                self.response = response

    def compileNN(self):
        # most basic LSTM for this shape input that I know of. Change to your liking.
        regressor = Sequential()

        # 1D CNN
        # reg...add(1DCNN)

        # Shape

        # LSTM
        regressor.add(LSTM(units=100, return_sequences=True, input_shape=(self.lookback, len(self.features))))

        regressor.add(LSTM(100))

        regressor.add(Dense(units=self.projectforward))

        regressor.compile(optimizer='adam', loss='mean_squared_error')

        return regressor

    def fitNN(self, data, verbose=1, suppressoutput=True):

        regressor = self.compileNN()
        [[xtest, xtrain], [ytest, ytrain]] = data
        print('fitting new LSTM for symbol: {}, response: {}'.format(self.underlying, self.response))
        history = regressor.fit(x=xtrain, y=ytrain, batch_size=20, epochs=10, verbose=verbose,
                                validation_data=(xtest, ytest), shuffle=False, class_weight=None,
                                sample_weight=None, initial_epoch=0, steps_per_epoch=None,
                                validation_steps=None, validation_batch_size=None, validation_freq=1)
        if not suppressoutput:
            # summarize history for loss
            plt.plot(history.history['loss'])
            plt.plot(history.history['val_loss'])
            plt.title('model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()
        self.validationloss = history.history['val_loss'][-1]
        return regressor

    def updateRegressor(self, data, datadescribe=None, BDinterval=None, traintotalratio=None):
        self.regressor = self.fitNN(data)
        self.datadescribe = datadescribe
        self.BDinterval = BDinterval
        self.traintotalratio = traintotalratio

    def saveRegressor(self, name, overwrite=True, folder='trained models'):

        self.modelfile = Path(folder) / (name + '.h5')
        self.metadatafile = Path(folder) / (name + '_metadata.txt')
        self.modelfolder = folder

        metadatadic = {
            'underlying': self.underlying,
            'train/total': self.traintotalratio,
            'lookback': self.lookback,
            'project forward': self.projectforward,
            'features': self.features,
            'response': self.response,
            'data': self.datadescribe.to_json(),
            'frequency': self.BDinterval,
            'loss': self.validationloss
        }

        if not os.path.exists(Path(folder)):
            os.mkdir(Path(folder))
        self.regressor.save(self.modelfile)
        with open(self.metadatafile, "w+") as outfile:
            json.dump(metadatadic, outfile)

        print('the regressor was saved for symbol: {}, response: {} and metadata was updated in the object and saved in json in\
              folder: {}'.format(self.underlying, self.response, self.modelfolder))

    def loadRegressor(self, name, folder='trained models'):

        self.modelfile = Path(folder) / (name + '.h5')
        self.regressor = load_model(self.modelfile)
        print('model loaded from {} into {}'.format(self.modelfile, self.regressor))

        with open(Path(folder) / (name + '_metadata.txt')) as f:
            metadata = json.load(f)
            self.metadatafile = Path(folder) / (name + '_metadata.txt')
            self.underlying = metadata['underlying']
            self.modelfolder = folder
            self.traintotalratio = metadata['train/total']
            self.BDinterval = metadata['frequency']
            self.datadescribe = pd.read_json(metadata['data'])
            self.lookback = metadata['lookback']
            self.projectforward = metadata['project forward']
            self.features = metadata['features']
            self.response = metadata['response']
            print('metadata was loaded from {} for symbol: {}, response: {}'
                  .format(Path(folder) / (name + '_metadata.txt'), self.underlying, self.response))

    def visNNperf(self, data, BD_interval, usetrainscaler=True, suppressoutput=True):

        timeoffset = pd.tseries.offsets.BusinessDay(BD_interval)
        resampled_dataset = data.resample(timeoffset).mean().fillna(method='ffill')[self.features]
        for feature in self.features:
            if usetrainscaler:
                minimum = self.datadescribe.loc['min', feature]
                maximum = self.datadescribe.loc['max', feature]
            else:
                minimum = resampled_dataset[feature].min()
                maximum = resampled_dataset[feature].max()
            resampled_dataset[feature] = (resampled_dataset[feature] - minimum) / (maximum - minimum)

        i = self.lookback
        totalLen = len(resampled_dataset)
        result_dataset = resampled_dataset.copy()
        result_dataset['prediction'] = None
        predloc = result_dataset.columns.get_loc('prediction')

        while i < totalLen - self.projectforward:
            xdata = resampled_dataset.iloc[i - self.lookback:i].values
            ypredict = self.regressor.predict(np.reshape(xdata, (1, self.lookback, len(self.features))))
            result_dataset.iloc[i:i + self.projectforward, predloc] = ypredict[0]
            i += self.projectforward
        if not suppressoutput:
            plt.plot(result_dataset[self.response], label='Actual')
            plt.plot(result_dataset['prediction'], label='Predicted')
            plt.legend()
            plt.show()
        return result_dataset

    def predictFuture(self, projection, data, suppressoutput=True):
        # ensure data is passed as a SORTED datetime indexed dataframe with all the needed features and all the rows have data
        timeoffset = pd.tseries.offsets.BusinessDay(self.BDinterval)
        allfeatures = [feature[:-5] for feature in self.features if feature.endswith("_grad")]
        for feature in self.features:
            allfeatures.append(feature) if feature not in allfeatures else allfeatures
        data = data.resample(timeoffset).mean().fillna(method='ffill')[allfeatures]
        featuresloc = [data.columns.get_loc(feature) for feature in self.features]
        feeddata = data.iloc[len(data) - self.lookback:len(data) + 1, featuresloc]
        for feature in self.features:
            minimum = self.datadescribe.at['min', feature]
            maximum = self.datadescribe.at['max', feature]
            feeddata[feature] = (feeddata[feature] - minimum) / (maximum - minimum)
        feeddata = np.reshape(feeddata.values, (1, self.lookback, len(self.features)))
        predictions = list(self.regressor.predict(feeddata)[0])
        minimum = self.datadescribe.at['min', self.response[0]]
        maximum = self.datadescribe.at['max', self.response[0]]
        predictions = [minimum + prediction * (maximum - minimum) for prediction in predictions]

        predcol = self.response[0] + '_Pred'
        data[predcol] = None

        if self.response[0].endswith('_grad'):
            integralcol = self.response[0][:-5] + '_Pred'
            data[integralcol] = None
            responseIsGradient = True
            lastintegral = data.iat[-1, data.columns.get_loc(self.response[0][:-5])]
        else:
            responseIsGradient = False
        currentpredtime = data.index[-1]
        while currentpredtime <= projection:
            try:
                currentpred = predictions.pop(0)
            except IndexError:
                print('Warning: This LSTM for {} cannot predict passed {} while a projection to {} is expected'.
                      format(self.underlying, currentpredtime, projection))
                break
            currentpredtime += timeoffset
            if responseIsGradient:
                currentintegral = (currentpred + 1) * lastintegral
                data = data.append(
                    pd.Series({predcol: currentpred, integralcol: currentintegral}, name=currentpredtime))
                # print('added currednt grad pred {} and integral {} to dataframe for {}'.format(currentpred, currentintegral, currentpredtime))
                lastintegral = currentintegral
            else:
                data = data.append(pd.Series({predcol: currentpred}, name=currentpredtime))

        if not suppressoutput:
            plt.plot(data[self.response].iloc[-100:], label='Actual')
            plt.plot(data['Prediction'], label='Predicted')
            plt.legend()
            plt.show()
        return data

################################################
def updateStockData(symbols, start, end=pd.to_datetime('today'), datafolder='Data'):
    dataDic = {}
    for symbol in symbols:
        try:
            data = web.DataReader(symbol, 'yahoo', start, end)
        except:
            data = pd.read_csv(Path(datafolder) / (symbol + '.csv'))
            print(
                f"unable to load stock data from Pandas data_reader API for {symbol}. Loaded the last saved local version instead.")
        dataDic.update({symbol: data})
        if not os.path.exists(Path(datafolder)):
            os.mkdir(Path(datafolder))
        data.to_csv(Path(datafolder) / (symbol + '.csv'))

    return dataDic

########################


def updateNetworks(symbols, startdate=pd.to_datetime('2005, January, 1'), response='Close_grad', lookback=60,
                   projectforward=60,
                   traintotalratio=0.75, BDinterval=10, features=['Close_grad', 'Volume', 'Volatility']):
    stockNNDict = {}
    datadic = updateStockData(symbols, startdate)
    for symbol in symbols:
        stockData = stockDataPrep(HistoricalData=datadic[symbol])
        (xdata, ydata, datadescribe) = stockData.createFeedData(BDinterval, lookback, projectforward=projectforward,
                                                                features=features, response=[response])
        [[xtest, xtrain], [ytest, ytrain]] = stockData.test_train_split((xdata, ydata),
                                                                        traintotalratio=traintotalratio,
                                                                        order='randomized', how='testmiddle')
        stockNN = stockLSTM(lookback, projectforward, features, underlying=symbol, response=[response])
        stockNN.updateRegressor([[xtest, xtrain], [ytest, ytrain]], datadescribe=datadescribe,
                                BDinterval=BDinterval,
                                traintotalratio=traintotalratio)
        stockNN.saveRegressor(symbol + '_' + response)
        ############
        # stockNN.visNNperf(stockData.reprocessData(BDinterval, gradientFeatures = ['Close']), BDinterval, suppressoutput = False)
        ##############
        stockNNDict.update({symbol: stockNN})

    return stockNNDict

########################
def loadNNFromFile(symbols, response='Close', folder='trained models'):
    NNDict = {}
    for symbol in symbols:
        stockNN = stockLSTM(loadfromfile=True, filestemname=symbol + '_' + response, folder=folder)
        NNDict.update({symbol: stockNN})
    return NNDict

########################

def updatePredictions(symbols, NNDict, projection, folders='trained models', response='Close'):
    PredictionsDict = {}
    datadic = updateStockData(symbols, pd.to_datetime('January, 1, 2000'))
    for symbol in symbols:
        newdata = stockDataPrep(datadic[symbol])
        newdata = newdata.reprocessData(1, gradientFeatures=['Close'])
        latestresponse = newdata[response][-1]
        stockNN = NNDict[symbol]
        Prediction = stockNN.predictFuture(projection, newdata)
        PredictionsDict.update({symbol: (Prediction, latestresponse)})
        print('predictions are updated for symbol: {}, response: {} up to: {}'.format(symbol, response, projection))
    return PredictionsDict
######################

def optionStrategy(Close, Volatility, Expiration):
    # Close and Volatility should be python tuples or lists as outputted by the updatePredictions function and contain
    # a dataframe including Close or Volatility Predictions and the second member is the CURRENT Close or Volatility value.
    if Expiration > Close[0].index[-1]:
        raise Exception("Option expiration is passed the point our current LSTM can predict.")
    today = pd.to_datetime('today')
    PredictionClose = Close[0][Close[0].index > today]
    PredictionClose = PredictionClose[PredictionClose.index <= Expiration]['Close_Pred']
    CurrentClose = Close[1]
    PredictionVolatility = Volatility[0][Volatility[0].index > today]
    PredictionVolatility = PredictionVolatility[PredictionVolatility.index <= Expiration]['Volatility_Pred']
    CurrentVolatility = Volatility[1]
    ClosePercentile = len(PredictionClose[PredictionClose.values < CurrentClose]) / len(PredictionClose)
    VolatilityPercentile = len(PredictionVolatility[PredictionVolatility.values < CurrentVolatility]) / len(
        PredictionVolatility)
    return ClosePercentile, VolatilityPercentile
