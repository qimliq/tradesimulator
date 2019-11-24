import numpy
import logging
from tradechecker import TradeChecker

from stocks import allstocks, stockgroup100, singlestock, stockgroupX, stockgroupY, stockgroupZ, stockgroupFav, stockgroupFavSma, stockgroupFavSma2,stockgroupFav2
from Asset import Asset
from Portfolio import Portfolio
import talib
import matplotlib.pyplot as pyplot

class Algo0(TradeChecker):

    def __init__(self, port):
        self.capital = port.capital
        self.CAPITAL_MAX = port.capital + 1
        self.portfolio = port


    def run(self):
        assets = []
        idx=0
        self.capital = self.CAPITAL_MAX
        self.moneyInStock = 0.0
        startIndex = self.startDateIndex

        self.setup_logger('algologger0', 'logs/algo0.txt', level=logging.INFO)
        algologger = logging.getLogger('algologger0')

        algologger.debug("\nTradeChecker Algo0")

        assets = self.portfolio.asset_list

        refAsset = Asset("STOCK1")

        s = numpy.where(refAsset.series.Index.values==startIndex)
        sindex = s[0][0]

        self.endIndex = refAsset.series.Index.values[-1]

        # last = 4400
        index = startIndex
        last  = self.endIndex
        min_amount = self.CAPITAL_MAX/len(assets)

        # index = 100000000
        while startIndex < last:
            for asset in assets:
                k = numpy.where(asset.series.Index.values==startIndex)
                if len(k[0]):
                    index = k[0][0]
                else:
                    continue
                close = asset.series.Close.values
                high  = asset.series.High.values
                low   = asset.series.Low.values

                step  = self.getStep(close[index-1])

                if asset.buynextday == 1 and low[index] + step < asset.buyprice:
                    if self.capital >= min_amount:
                        asset.stockcount += (min_amount/asset.buyprice)
                        algologger.info("Bought:" + asset.name + " :" + str(asset.buyprice)  + " " + asset.series.Date.values[index])
                        self.capital -= min_amount
                        asset.buyprice = 0.0
                        asset.buynextday = 0
                    else:
                        #algologger.info("NO Capital left ------------------------")
                        asset.buyprice = 0.0
                        asset.buynextday = 0

                if asset.sellnextday == 1 and high[index] - step > asset.sellprice:
                    amount = asset.stockcount * asset.sellprice
                    algologger.info("                                                  Sold:" + asset.name + " :" + str(asset.sellprice) + " " + asset.series.Date.values[index])
                    self.capital += amount
                    asset.sellnextday = 0
                    asset.sellprice = 0.0
                    asset.stockcount = 0


                if (asset.stockcount == 0):
                    algologger.info("buy next day: " + asset.name + " " + asset.series.Date.values[index])
                    asset.buynextday = 1
                    asset.buyprice = close[index] - (5 * step)


            sindex += 1
            startIndex= refAsset.series.Index.values[sindex]

        for asset in assets:
            close = asset.series.Close.values
            self.moneyInStock += (asset.stockcount * close[-1])

        final = "Algo0[Buy and Hold]: Cap: %0.2f    MiS: %0.2f   P/L: %0.2f  Total: %0.2f \n" % (
            self.capital, self.moneyInStock, self.profit_loss, self.capital + self.moneyInStock)
        algologger.info(final)

        return (self.capital + self.moneyInStock)
