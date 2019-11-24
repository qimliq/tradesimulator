from pandas import read_csv


class Asset:

    path = "csv/"
    name = ""
    series = ""

    stockcount = 0.0
    amount = 0.0
    sellprice = 0.0
    buyprice = 0.0
    lastdate = 0
    buynextday = 0
    sellnextday = 0
    profit = 0.0
    shortcount = 0
    shortamount = 0.0
    sellshort = 0
    buylock = 1
    buycount = 0
    nosell = False
    added_count = 0
    added_price = 0.0
    removed_count = 0
    removed_price = 0.0
    minstop = 0.0

    def __init__(self,
                 nm,sc = 0,
                 amt = 0,
                 pl=0,
                 nosell=False):
        self.name = nm
        self.stockcount = sc
        self.amount = amt
        self.series = read_csv(self.path + nm + ".csv", sep=',', header=0)
        self.profit = pl
        self.nosell = nosell



    def __del__(self):
        self.name = ""


    def GetName(self):
        return self.name

    def AddStock(self,added=0,added_price=0.0):
        self.added_count = added
        self.added_price = added_price

    def RemoveStock(self,removed=0,removed_price=0.0):
        self.removed_count = removed
        self.removed_price = removed_price

