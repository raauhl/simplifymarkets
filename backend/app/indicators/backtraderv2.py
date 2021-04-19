from datetime import datetime
import backtrader as bt
import sys


#flask working
'''
def getInput(stock,timeframe,indicators1,comparator,indicators2):
    
    
    print(input_data["stock"])
    return input_data["stock"]
'''

# Create a subclass of Strategy to define the indicators and logic

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


def getInput(stock,timeframe,indicators1,comparator,indicators2):
    print('#################################', file=sys.stderr)
    print(stock, file=sys.stderr)
    input_data = {"stock":stock,
              "timeframe":timeframe,
              "indicators1": indicators1,
              "comparator" :comparator,
              "indicators2": indicators2
              }
    cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = bt.feeds.YahooFinanceData(dataname=stock,
                                 fromdate=datetime(2011, 1, 1),
                                 todate=datetime(2013, 12, 31))

cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.run()  # run it all
#cerebro.plot()  # and plot it with a single command

if __name__ == '__main__':
    # Get arguments from user
    print('#################################', file=sys.stderr)
    stock= sys.argv[1]
    timeframe= sys.argv[2]
    indicators1= sys.argv[3]
    comparator= sys.argv[4]
    indicators2= sys.argv[5]
    getInput(stock,timeframe,indicators1,comparator,indicators2)
