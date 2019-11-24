import numpy
import logging

from stocks import allstocks, stockgroup100, singlestock, stockgroupX, stockgroupY, stockgroupZ, stockgroupFav, stockgroupFavSma, stockgroupFavSma2,stockgroupFav2
from Asset import Asset
from Portfolio import Portfolio
import talib
import matplotlib.pyplot as pyplot

class TradeChecker:
    startDateIndex = 1120104
    startDateIndex = 1170908
    endIndex = 0
    capital = 20000.0
    moneyInStock = 0.0
    minAmount = 10000.0
    CAPITAL_MAX = 20001.0
    teststocks = stockgroupY
    portfolio = None

    profit_loss = 0.0
    commission_rate = 0.002

    def __init__(self, port):
        self.capital = port.capital
        self.CAPITAL_MAX = port.capital + 1
        self.portfolio = port

    def getStep(self,price):
        if price < 5:
            return 0.01
        elif price < 10:
            return 0.02
        elif price < 25:
            return 0.05
        elif price < 50:
            return 0.10
        elif price < 100:
            return 0.25
        elif price < 250:
            return 0.5
        elif price < 500:
            return 1.00
        elif price < 1000:
            return 2.00
        else:
            return 5.00



    def setup_logger(self, logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(message)s')
        fileHandler = logging.FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)
        # if level == logging.DEBUG:
        #     l.addHandler(streamHandler)

