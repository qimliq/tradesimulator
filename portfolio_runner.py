from Asset import Asset
from Portfolio import Portfolio
from tradechecker import TradeChecker
from Asset import Asset
from stocks import stockgroupY

def portfolio_checker():
    teststocks = stockgroupY

    port = Portfolio(0)

    asset = Asset("STOCK1", pl=-967)
    port.asset_list.append(asset)


    for stock in teststocks:
        port.add_asset(Asset(stock))

    num = 1

    asset = Asset("STOCK2", num, (num * 3.05),nosell=True)
    # asset.AddStock(50000,3.05)
    port.asset_list.append(asset)

    port.capital = 38140

    tc = TradeChecker(port)
    tc.startDateIndex = 1180329

    tc.algo8(buyhunger=0,sellhunger=0,showgraph=False,endIndex=0)
    # tc.algo6()

portfolio_checker()
