import numpy
import logging
from tradechecker import TradeChecker

from stocks import allstocks, stockgroup100, singlestock, stockgroupX, stockgroupY, stockgroupZ, stockgroupFav, stockgroupFavSma, stockgroupFavSma2,stockgroupFav2
from Asset import Asset
from Portfolio import Portfolio
import talib
import matplotlib.pyplot as pyplot

class Algo3(TradeChecker):

    def __init__(self, port):
        self.capital = port.capital
        self.CAPITAL_MAX = port.capital + 1
        self.portfolio = port

    def run(self):
        assets = []
        idx = 0
        self.capital = self.CAPITAL_MAX
        self.moneyInStock = 0.0
        startIndex = self.startDateIndex

        self.setup_logger('algologger3', 'logs/algo3.txt', level=logging.INFO)
        algologger = logging.getLogger('algologger3')

        algologger.debug("\nTradeChecker Algo3")

        assets = self.portfolio.asset_list

        refAsset = Asset("STOCK1")

        s = numpy.where(refAsset.series.Index.values == startIndex)
        sindex = s[0][0]

        self.endIndex = refAsset.series.Index.values[-1]

        # last = 4400
        index = startIndex
        last = self.endIndex

        buyhungerrate = 0
        sellhungerrate = 0

        min_amount = self.minAmount

        # index = 100000000
        while startIndex <= last:
            money_in_stock = 0.0
            for asset in assets:
                k = numpy.where(asset.series.Index.values == startIndex)
                if len(k[0]):
                    index = k[0][0]
                else:
                    continue
                close = asset.series.Close.values
                high = asset.series.High.values
                low = asset.series.Low.values

                step = self.getStep(close[index - 1])

                if asset.buynextday > 0 and low[index] < asset.buyprice:
                    buy_amount = asset.buyprice * asset.buycount
                    if self.capital >= buy_amount:
                        asset.stockcount += asset.buycount
                        algologger.info("%10s: %5s %10.2f %5d %5d" % (
                            "Bought", asset.name, asset.buyprice, asset.buycount, asset.stockcount))
                        self.capital -= buy_amount
                        cost = (buy_amount * self.commission_rate)
                        self.capital -= cost
                        asset.buyprice = 0.0
                        asset.buynextday = 0
                        asset.buycount = 0
                        asset.amount += buy_amount
                    else:
                        # algologger.debug("NO Capital left ------------------------")
                        asset.buyprice = 0.0
                        asset.buynextday = 0
                        asset.buycount = 0

                if asset.sellnextday > 0 and high[index] > asset.sellprice:
                    amount = asset.stockcount * asset.sellprice
                    m = (asset.amount / asset.stockcount)
                    algologger.info("%10s: %5s %10.2f %10.2f p/l:%10.2f" % (
                        "Sold", asset.name, asset.sellprice, m, (asset.sellprice - m) * asset.stockcount))
                    self.profit_loss += (asset.sellprice - m) * asset.stockcount
                    self.capital += amount
                    cost = (amount * self.commission_rate)
                    self.capital -= cost
                    asset.amount = 0
                    asset.sellnextday = 0
                    asset.sellprice = 0.0
                    asset.stockcount = 0

            order_limit = self.capital

            for asset in assets:
                k = numpy.where(asset.series.Index.values == startIndex)
                if len(k[0]):
                    index = k[0][0]
                else:
                    continue
                sma50 = talib.SMA(asset.series.Close.values, timeperiod=50)
                close = asset.series.Close.values
                high = asset.series.High.values
                low = asset.series.Low.values

                step = self.getStep(close[index - 1])
                valp = high[index - 1] - ((high[index - 1] - low[index - 1]) * 0.25)
                valn = low[index - 1] + ((high[index - 1] - low[index - 1]) * 0.25)

                # BUY conditions
                if close[index] > sma50[index] and close[index - 1] > valp and close[index] > high[index - 1]:
                    if asset.stockcount == 0:
                        asset.buynextday = 1
                        asset.buyprice = close[index] - (buyhungerrate * step)
                        asset.buycount = min_amount // asset.buyprice
                        order_limit -= min_amount
                        algologger.debug("Buy-1: %s %s %0.2f #: %d" % (
                            asset.name, asset.series.Date.values[index], asset.buyprice, asset.buycount))

                # SELL conditions
                if close[index] < sma50[index] and close[index - 1] < valn and close[index] < low[index - 1]:
                    if asset.stockcount > 0:
                        asset.sellnextday = 1
                        asset.sellprice = close[index] + (sellhungerrate * step)
                        algologger.debug(
                            "Sell-1: %s %s %0.2f" % (asset.name, asset.series.Date.values[index], asset.sellprice))

                money_in_stock += asset.stockcount * close[index]

            if sindex < len(refAsset.series.Index.values) - 1:
                sindex += 1
            else:
                break
            startIndex = refAsset.series.Index.values[sindex]
            algologger.debug("-------------------------------------------------------------")

        algologger.info("==Name=====Count=====Amount=======Mean========Close===")
        for asset in assets:
            close = asset.series.Close.values
            if asset.stockcount > 0:
                mean = asset.amount / asset.stockcount
            else:
                mean = 0.0
            algologger.info("[%5s]: %6d  %8d    %10.2f    %8.2f" % (
                asset.name, asset.stockcount, asset.stockcount * close[-1], mean, close[-1]))
            self.moneyInStock += (asset.stockcount * close[-1])
        algologger.info("========================================================")

        final = "Algo3[High 25percent ]: Cap: %0.2f    MiS: %0.2f   P/L: %0.2f  Total: %0.2f \n" % (
            self.capital, self.moneyInStock, self.profit_loss, self.capital + self.moneyInStock)
        algologger.info(final)

        return (self.capital + self.moneyInStock)

