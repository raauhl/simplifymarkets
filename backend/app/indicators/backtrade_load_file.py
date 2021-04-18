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




#Set data parameters and add to Cerebro
data = bt.feeds.YahooFinanceCSVData(
    dataname=STOCK_ID[0],
    fromdate=datetime.datetime(2020, 5, 5),
    timeframe=bt.TimeFrame.Days,
    todate=datetime.datetime(2020, 6, 12))
    #settings for out-of-sample data
    #fromdate=datetime.datetime(2018, 1, 1),
    #todate=datetime.datetime(2019, 12, 25))


#starting cerebro engine
cerebro = bt.Cerebro(optreturn=False)
cerebro.addwriter(bt.WriterFile, csv=True, out="trade_history.csv")
cerebro.adddata(data)
cerebro.addstrategy(btstrats.SMA_CrossOver)

# Analyzer
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

thestrats = cerebro.run()
thestrat = thestrats[0]

print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
#cerebro.addstrategy(STRATEGY[0],pfast=10,pslow=30)
#cerebro.run()
#cerebro.plot()