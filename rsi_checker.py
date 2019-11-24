import talib
from pandas import Series, TimeSeries, read_csv
from scipy import signal

import matplotlib.pyplot as pyplot

import peakutils
from stocks import allstocks, stockgroup100



def check_rsi():

    for stock in allstocks:
        series = read_csv("csv/" + stock + ".csv", sep=',', header=0)

        close = series.Close.values

        rsi = talib.RSI(close, timeperiod=21)

        #print(rsi[-1])

        peaks = peakutils.indexes(close[-500:], thres=0.1, min_dist=50)

        valleys = peakutils.indexes(-1 * close[-500:], thres=0.1, min_dist=50)

        ema200 = talib.EMA(close, timeperiod=200)

        #print(stock)

        if rsi[-2] < 30 and rsi[-1] > 30 and close[-1] > ema200[-1]:
            print(stock + " --- was < 30 and now > 30 ")
            #print(rsi[-1])

        if rsi[-1] < 30 and close[-1] > ema200[-1]:
            print(stock + " --- still < 30 ")
            #print(rsi[-1])

        if rsi[-2] > 70 and rsi[-1] < 70:
            print(stock + " +++ ")
            #print(rsi[-1])

    print("check_rsi")


check_rsi()