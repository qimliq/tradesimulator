from Algo0 import Algo0
from Algo1 import Algo1
from Algo10 import Algo10
from Algo2 import Algo2
from Algo3 import Algo3
from Algo4 import Algo4
from Algo5 import Algo5
from Algo6 import Algo6
from Algo7 import Algo7
from Algo8 import Algo8
from Algo9 import Algo9
from Asset import Asset
from Portfolio import Portfolio
from tradechecker import TradeChecker
from stocks import stockgroupY,allstocks,stockgroupX,stockgroup100, singlestock, \
    stockgroupFav,stockgroupFav2,stockgroupFavSma,stockgroupFavSma2,stockgroupZ, euronext, stockgroupW

teststocks = allstocks

def trade_run(num):
    # teststocks = imkbY
    port = Portfolio(100001)

    for stock in teststocks:
        port.add_asset(Asset(stock))


    if num == 0:
        tc = Algo0(port)
    if num == 1:
        tc = Algo1(port)
    if num == 2:
        tc = Algo2(port)
    if num == 3:
        tc = Algo3(port)
    if num == 4:
        tc = Algo4(port)
    if num == 5:
        tc = Algo5(port)
    if num == 6:
        tc = Algo6(port)
    if num == 7:
        tc = Algo7(port)
    if num == 8:
        tc = Algo8(port)
    if num == 9:
        tc = Algo9(port)
    if num == 10:
        tc = Algo10(port)

    tc.startDateIndex = 1180102
    t = tc.run()
    print("algo"+str(num)+": %0.2f" % (t))


    port.asset_list.clear()
    del port
    del tc

for teststocks in [stockgroupY]:
    for i in [10,9,8,0]:
        trade_run(i)
    print("---------------")
