
import backtrader as bt
import sys
import inspect
import array
import re
import backtrader.analyzers as btanalyzers


from datetime import date

class SmaCross(bt.Strategy):
    
    params = {"stop_loss": 0.02, "targetpercentage" : 0.02}
    
    #def log(self, arg):
     #   if not self.p.backtest:
     #       print('{} {}'.format(self.datetime.datetime(), arg))
            
    def __init__(self, ind1, ind2, comp): 
        self.ml_log = []
        strategy_data = []
        input = ind1
        #stoploss = stop_loss
        #print("stoploss inside class is  ", stoploss)
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
            if strategy[0] == "boll":
                boll = bt.indicators.BollingerBands(period=int(strategy[1][0]), devfactor=int(strategy[1][1]))
                strategylist.append(boll)

        self.crossover = bt.ind.CrossOver(strategylist[0], strategylist[1])
        #print("stoploss is ", stoploss)
        
    def notify_order(self, order):
        if not order.status == order.Completed:
            return  # discard any other notification

        if not self.position:  # we left the market
            print('SELL@price: {:.2f}'.format(order.executed.price))
            return
            
        if order.status in [order.Completed]:
            if order.isbuy():
               # self.log(
                #    'BUY EXECUTED, Price: %.5f, Cost: %.2f, Comm %.2f' %
                #    (order.executed.price,
                 #    order.executed.value,
                #     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.5f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)
        #print('BUY @price: {:.2f}'.format(order.executed.price))
        #try:
        #    stop_price = order.executed.price * (1.0 - float(self.p.stop_loss))
        #    print("stoploss is ", stop_price)
        #    self.sell(exectype=bt.Order.Stop, price=stop_price)
        #except NameError:
        #    print("stoploss is not set ")
       # try:
            #target_price = order.executed.price * (1.0 + float(self.p.targetpercentage))
            #print("target price  is ", target_price)
            #self.sell(exectype=bt.Order.Stop, price=target_price)
        #except NameError:
           # print("target_price is not set ")
        
    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
                #stop_price = order.executed.price * (1.0 - float(self.p.stop_loss))
                #self.sell(exectype=bt.Order.Stop, price=stop_price)

        elif self.crossover < 0:
            self.close()  # close long position



def getInput(stock,startday,endday,indicators1,comparator,indicators2,stoploss,targetprofit):

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
    print("stoploss is ", stoploss)
    cerebro.addstrategy(SmaCross , ind1=indicators1, ind2=indicators2,comp = comparator,stop_loss = stoploss,targetpercentage = targetprofit)
   # cerebro.addanalyzer(bt.analyzers.SharpeRatio, timeframe=TimeFrame.Years)
   # cerebro.addanalyzer(bt.analyzers.Calmar, timeframe=TimeFrame.Years)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.AnnualReturn)
    #cerebro.addanalyzer(bt.analyzers.PyFolio, timeframe=TimeFrame.Days, compression=1)
    cerebro.addanalyzer(bt.analyzers.Transactions)
    cerebro.addanalyzer(bt.analyzers.Returns)
    
    optreturn = cerebro.run()  # run it all
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    totalvalue = cerebro.broker.getvalue()
    #for strat in results:
    #    print('='*79)
    #    print(strat.__class__.__name__)

     #   # Analyzers results
     ##   strat.analyzers.annualreturn.print()
      #  strat.analyzers.drawdown.print()
      #  strat.analyzers.sharperatio.print()
      #  strat.analyzers.returns.print()

        # pyfolio
       # pyfoliozer = strat.analyzers.getbyname('pyfolio')
       # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

        # Perfomance
        #pf.show_perf_stats(returns=returns)
    cerebro.plot()
    # graph.savefig('graph.png')
    list_toreturn = { "totalvalue": totalvalue}
    #print('Sharpe Ratio:', optreturn[0].analyzers.mysharpe.get_analysis())
    return list_toreturn

    

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






