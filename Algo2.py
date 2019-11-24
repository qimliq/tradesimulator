import numpy
import logging
from tradechecker import TradeChecker

from stocks import allstocks, stockgroup100, singlestock, stockgroupX, stockgroupY, stockgroupZ, stockgroupFav, stockgroupFavSma, stockgroupFavSma2,stockgroupFav2
from Asset import Asset
from Portfolio import Portfolio
import talib
import matplotlib.pyplot as pyplot

class Algo2(TradeChecker):

    def __init__(self, port):
        self.capital = port.capital
        self.CAPITAL_MAX = port.capital + 1
        self.portfolio = port

    def run(self):
        assets = []
        idx = 0

        self.setup_logger('algologger2', 'logs/algo2.txt', level=logging.DEBUG)
        algologger = logging.getLogger('algologger2')

        self.capital = self.CAPITAL_MAX
        self.moneyInStock = 0.0
        self.profit_loss = 0.0
        startIndex = self.startDateIndex

        assets = self.portfolio.asset_list

        refAsset = Asset("STOCK1")

        s = numpy.where(refAsset.series.Index.values == startIndex)
        sindex = s[0][0]

        self.endIndex = refAsset.series.Index.values[-1]

        # last = 4400
        index = startIndex
        last = self.endIndex

        buyhungerrate = 5
        sellhungerrate = 5

        cap = []
        min_amount = self.minAmount

        while startIndex <= last:
            order_limit = self.capital
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

                step = self.getStep(close[index])

                # min_amount = self.capital/10

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
                sma20 = talib.SMA(asset.series.Close.values, timeperiod=20)
                sma200 = talib.SMA(asset.series.Close.values, timeperiod=200)
                close = asset.series.Close.values

                step = self.getStep(close[index])

                # BUY conditions
                if self.capital >= self.minAmount and order_limit >= min_amount:
                    if close[index] > sma200[index] and close[index] > sma20[index] and sma20[index] > sma200[index] and \
                                    sma20[index] < (sma200[index] * 1.1) and asset.stockcount == 0:
                        asset.buynextday = 4
                        asset.buyprice = close[index]
                        asset.buycount = min_amount // asset.buyprice
                        order_limit -= min_amount
                        algologger.debug("Buy-4: %s %s bp:%0.2f #:%d" % (
                        asset.name, asset.series.Date.values[index], asset.buyprice, (min_amount // asset.buyprice)))
                    elif close[index] > sma200[index] and close[index] > sma20[index] and sma20[index] > sma200[
                        index] and asset.stockcount > 0:
                        meanprice = asset.amount / asset.stockcount
                        if close[index] < (meanprice * 1.5):
                            asset.buynextday = 3
                            asset.buyprice = close[index]
                            asset.buycount = min_amount // asset.buyprice
                            order_limit -= min_amount
                            algologger.debug("Buy-3: %s %s bp:%0.2f #:%d" % (
                            asset.name, asset.series.Date.values[index], asset.buyprice,
                            (min_amount // asset.buyprice)))
                    elif close[index] <= (sma200[index] * 0.65):
                        asset.buynextday = 2
                        asset.buyprice = close[index] - (buyhungerrate * step)
                        order_limit -= min_amount
                        asset.buycount = min_amount // asset.buyprice
                        algologger.debug("Buy-2: %s %s bp:%0.2f #:%d" % (
                        asset.name, asset.series.Date.values[index], asset.buyprice, (min_amount // asset.buyprice)))
                    elif close[index - 1] <= (sma200[index - 1] * 1.02) and close[index] > (sma200[index] * 1.02):
                        asset.buynextday = 1
                        asset.buyprice = close[index] - (buyhungerrate * step)
                        order_limit -= min_amount
                        asset.buycount = min_amount // asset.buyprice
                        algologger.debug("Buy-1: %s %s bp:%0.2f #:%d" % (
                        asset.name, asset.series.Date.values[index], asset.buyprice, (min_amount // asset.buyprice)))

                # SELL conditions
                if close[index - 1] < (sma200[index - 1] * 0.98) and close[index] < (
                    sma200[index] * 0.98) and asset.stockcount > 0:
                    asset.sellnextday = 1
                    asset.sellprice = close[index] + (sellhungerrate * step)
                    algologger.debug(
                        "Sell-1: %s %s   sp:%0.2f" % (asset.name, asset.series.Date.values[index], asset.sellprice))
                elif asset.stockcount > 0:
                    meanprice = asset.amount / asset.stockcount
                    if close[index] > (meanprice * 1.5):
                        asset.sellprice = close[index]
                        asset.sellnextday = 2
                        asset.buynextday = 0
                        algologger.debug(
                            "Sell-2: %s %s   sp:%0.2f" % (asset.name, asset.series.Date.values[index], asset.sellprice))

                money_in_stock += asset.stockcount * close[index]

            if sindex < len(refAsset.series.Index.values) - 1:
                sindex += 1
            else:
                break
            startIndex = refAsset.series.Index.values[sindex]
            cap.append(self.capital + money_in_stock)
            # algologger.info(str(self.capital + money_in_stock) + " " + str(startIndex))
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

        final = "Algo2[Sma20 and Sma200]: Cap: %0.2f    MiS: %0.2f   P/L: %0.2f  Total: %0.2f \n" % (
            self.capital, self.moneyInStock, self.profit_loss, self.capital + self.moneyInStock)
        algologger.info(final)
        # pyplot.plot(cap)
        # pyplot.show()
        return (self.capital + self.moneyInStock)

