from datetime import datetime
import backtrader as bt

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = ( ('pslow', None ), ('pfast', None), )
    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        self.dataclose = self.datas[0].close

    def prenext(self):
        print('prenext:: current period:', len(self))

    def nextstart(self):
        print('nextstart:: current period:', len(self))
        # emulate default behavior ... call next
        self.next()

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                #self.log('buy: ', self.dataclose[0])
                self.buy()  # enter long
                
        elif self.crossover < 0:  # in the market & cross to the downside
            #self.log('sell ', self.dataclose[0])
            self.close()  # close long position

