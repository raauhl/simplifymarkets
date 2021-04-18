import datetime
import backtrader as bt
from sma import SmaCross
import backtrader.strategies as btstrats
import backtrader.analyzers as btanalyzers

input_strategy = []
input_strategy.append("SmaCross")
logfile =  str(input_strategy[0]) + '.csv'

STRATEGY = [] 
STRATEGY.append( SmaCross )

STOCK_ID = []
STOCK_ID.append("..\\resources\\MAHABANK.NS.csv")



if __name__ == '__main__':

    cerebro = bt.Cerebro(optreturn=False)

    cerebro.addstrategy(SmaCross,pslow=10,pfast=30)
#Set data parameters and add to Cerebro
data = bt.feeds.YahooFinanceCSVData(
    dataname=STOCK_ID[0],
    fromdate=datetime.datetime(2020, 4, 24),
    #timeframe=bt.TimeFrame.Days,
    todate=datetime.datetime(2021, 4, 12))
    #settings for out-of-sample data
    #fromdate=datetime.datetime(2018, 1, 1),
    #todate=datetime.datetime(2019, 12, 25))

#added resample data for converting to weeks
#cerebro.resampledata(data, timeframe=bt.TimeFrame.Weeks, name='weeks')

# added logger
cerebro.addwriter(bt.WriterFile, csv=True, out="trade_history.csv")

#adding data
cerebro.adddata(data)


#cerebro.optstrategy(SMA_CrossOver, period=xrange(10, 30), factor=3.5)

# Analyzer
#cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

cerebro.run()
#thestrat = thestrats[0]

print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
#cerebro.addstrategy(STRATEGY[0],pfast=10,pslow=30)
#cerebro.run()
#cerebro.plot() 