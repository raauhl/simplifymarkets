from datetime import datetime
import backtrader as bt
import importlib
from dynamic import DynamicArray
#moduleName = input('dynamic')
importlib.import_module('dynamic')

#memory allocation
STRATEGY = DynamicArray()
# Append new element
STRATEGY.append("SmaCross")
stra_id=len(STRATEGY)

STOCK_ID = DynamicArray()
# Append new element
STOCK_ID.append("..\\resources\\MAHABANK.NS.csv")
stock_number=len(STOCK_ID)


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


print(STOCK_ID[0])
data = bt.feeds.YahooFinanceData(dataname=STOCK_ID[0],
                                 fromdate=datetime(2020, 1, 1),
                                 todate=datetime(2021, 3, 21))

cerebro = bt.Cerebro() 
cerebro.adddata(data)  # Add the data feed

'''
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.optstrategy(VolumeWeightedAveragePrice, idx=[0, 1])
results = cerebro.run(maxcpus=args.maxcpus, optreturn=args.optreturn)
cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(STRATEGY,pfast=10,pslow=40)  # Add the trading strategy
'''

cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command


