from datetime import datetime
import backtrader as bt

STOCK_ID = "resources\MAHABANK.NS.csv"
data = bt.feeds.YahooFinanceData(dataname=STOCK_ID,
                                 fromdate=datetime(2020, 5, 6),
                                 todate=datetime(2021, 3, 23))
								 
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.optstrategy(VolumeWeightedAveragePrice, idx=[0, 1])
results = cerebro.run(maxcpus=args.maxcpus, optreturn=args.optreturn)
cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(SmaCross,pfast=10,pslow=40)  # Add the trading strategy
