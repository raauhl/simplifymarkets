import backtrader as bt
import sys
import inspect
import array
import re
from datetime import date

class SmaCross(bt.Strategy):

    def __init__(self,ind1, ind2,comp): 
        strategy_data = []
        input = ind1
        print(input)
        position = re.search( '\(', input)
        strategy1 = input[0:position.start()]
        position2 = re.search('\)', input)
        mystring = input[position.start()+1:position2.start()]
        strategy_data.append([strategy1,mystring.split(",")])
        print(strategy_data)
        
        input = ind2
        print(input)
        
        position = re.search( '\(', input)
        strategy2 = input[0:position.start()]
        position2 = re.search('\)', input)
        mystring = input[position.start()+1:position2.start()]
        strategy_data.append([strategy2, mystring.split(",")])
        print("strategy is ##", strategy_data)
       
        strategylist = []
        for i,strategy in enumerate(strategy_data):
            if strategy[0] == "sma":
                sma = bt.ind.SMA(period=int(strategy[1][0]))
                strategylist.append(sma)

        self.crossover = bt.ind.CrossOver(strategylist[0], strategylist[1])

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position



def getInput(stock,startday,endday,indicators1,comparator,indicators2):

    startdate = date.fromisoformat(startday)
    enddate = date.fromisoformat(endday)
    if comparator == 'lessthan':
        comaprator = '<'
    elif comparator == 'greaterthan':
        comaprator = '>'
    else:
         comaprator = '='
    
    strategy_data = []
    #seperating strategy to name and parameters like sma(10) break to sma , 10
    input = indicators1
    position = re.search( '\(', input)
    strategy1 = input[0:position.start()]
    position2 = re.search('\)', input)
    mystring = input[position.start():position2.start()]
    strategy_data.append([strategy1,mystring.split(",")])
    print(strategy_data)
    
    input = indicators2
    position = re.search( '\(', input)
    strategy2 = input[0:position.start()]
    position2 = re.search('\)', input)
    mystring = input[position.start():position2.start()]
    strategy_data.append([strategy2, mystring.split(",")])
    print("strategy is {}", strategy_data)

 # create a "Cerebro" engine instance

# Create a data feed
    data = bt.feeds.YahooFinanceData(dataname = stock,
                                 fromdate=startdate,
                                 todate=enddate)
    cerebro = bt.Cerebro() 
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.adddata(data)  # Add the data feed
    cerebro.addstrategy(SmaCross , ind1=indicators1, ind2=indicators2,comp = comparator)
    optreturn = cerebro.run()  # run it all
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    totalvalue = cerebro.broker.getvalue()
    list_toreturn = { "totalvalue": totalvalue}
    return list_toreturn

    cerebro.plot()

if __name__ == '__main__':

    # Get arguments from user
    print('#################################')
    stock= str(sys.argv[1])
    startdate= date.fromisoformat(sys.argv[2])
    enddate = date.fromisoformat(sys.argv[3])
    indicators1 = sys.argv[4]
    comparator = sys.argv[5]
    if comparator == 'lessthan':
        comaprator = '<'
    elif comparator == 'greaterthan':
        comaprator = '>'
    else:
         comaprator = '='
    indicators2= sys.argv[6]
    final_portfolio = getInput(stock,startdate,enddate,indicators1,comparator,indicators2)
    print('Return value is %.2f' % final_portfolio)






