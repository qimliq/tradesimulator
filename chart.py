import talib
from pandas import Series, TimeSeries, read_csv
import matplotlib.pyplot as pyplot
import peakutils
from stocks import allstocks,stockgroup100

def charter():

    print("grafi")

    series = read_csv("csv/STOCK1.csv", sep=',', header=0)

    #print(series[-5:])

    close = series.Close.values
    #print(close[-5:])

    sma20 = talib.SMA(close, timeperiod=20)
    sma50 = talib.SMA(close, timeperiod=200)

    # Two subplots, the axes array is 1-d
    # f, axarr = pyplot.subplots(2, sharex=True)
    # axarr[0].plot(close[-1000:])
    # axarr[1].plot(sma20[-1000:])
    # axarr[1].plot(sma50[-1000:])
    # axarr[0].set_title('Sharing X axis')
    # pyplot.show()

    pyplot.plot(close[-5000:])
    pyplot.plot(sma20[-5000:])
    pyplot.plot(sma50[-5000:])
    pyplot.show()

charter()