import talib
from pandas import Series, TimeSeries, read_csv
import matplotlib.pyplot as pyplot
import peakutils
from stocks import allstocks,stockgroup100

def grafi():

    for stock in stockgroup100:
        series = read_csv("csv/" + stock + ".csv", sep=',', header=0)

        close = series.Close.values

        rsi = talib.RSI(close, timeperiod=21)

        #print(rsi[-1])

        peaks = peakutils.indexes(close[-500:], thres=0.1, min_dist=50)

        valleys = peakutils.indexes(-1 * close[-500:], thres=0.1, min_dist=50)

        #print(stock)

        if rsi[-2] < 40 and rsi[-1] > 40:
            print(stock + " --- ")
            #print(rsi[-1])

        if rsi[-2] > 70 and rsi[-1] < 70:
            print(stock + " +++ ")
            #print(rsi[-1])

    print("grafi")

    series =read_csv("csv/ASML.csv", sep=',', header=0)

    #print(series[-5:])

    close = series.Close.values
    #print(close[-5:])

    rsi = talib.RSI(close, timeperiod=20)

    #print(rsi[-5:])

    peaks = peakutils.indexes(close[-500:], thres=0.1, min_dist=10)

    valleys = peakutils.indexes(-1 * close[-500:], thres=0.1, min_dist=10)

    # pyplot.plot(close[-500:])

    #print(close[peaks - 500])



    # Two subplots, the axes array is 1-d
    f, axarr = pyplot.subplots(2, sharex=True)
    axarr[0].plot(close[-500:])
    axarr[0].plot(peaks,close[peaks - 500], 'or')
    axarr[0].plot(valleys, close[valleys - 500], 'og')
    axarr[0].set_title('Sharing X axis')
    axarr[1].plot(rsi[-500:],color='g')

    pyplot.show()


grafi()