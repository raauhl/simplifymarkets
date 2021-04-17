from datetime import datetime
import backtrader as bt
from dynamic import DynamicArray
from sma import SmaCross
from vvap import vvap

#moduleName = input('dynamic')


STRATEGY = [] 
STRATEGY.append( SmaCross )

STOCK_ID = []
STOCK_ID.append("..\\resources\\MAHABANK.NS.csv")

datestart = datetime.datetime.strptime('2020, 5, 17','%Y/%m/%d')
dateend = datetime.datetime.strptime('2021, 3, 17','%Y/%m/%d')

data = bt.feeds.GenericCSVData(
        dataname=STOCK_ID[0],
     
        fromdate=datestart,
        todate=dateend
    )
cerebro = bt.Cerebro() 
cerebro.adddata(data)  # Add the data feed

'''
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.optstrategy(VolumeWeightedAveragePrice, idx=[0, 1])
results = cerebro.run(maxcpus=args.maxcpus, optreturn=args.optreturn)
cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(STRATEGY,pfast=10,pslow=40)  # Add the trading strategy
'''
cerebro.addstrategy(STRATEGY[0])  # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command


