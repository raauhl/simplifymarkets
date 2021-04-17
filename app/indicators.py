from datetime import datetime
import backtrader as bt

# Create a subclass of Strategy to define the indicators and logic

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    #params = dict(
    #    pfast=10,  # period for the fast moving average
  #      pslow=30   # period for the slow moving average
   # )
    params = (('pfast',None), ('pslow', None),)
    def __init__(self):
        self.pfast = self.params.pfast
        self.pslow = self.params.pslow
        sma1, sma2 = bt.ind.SMA(pfast), bt.ind.SMA(pslow)
        crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

class BB(bt.Strategy):
    params = (('period',None), ('devfactor', None),)
    def __init__(self):
        self.period = self.params.period
        self.devfactor = self.params.devfactor
        self.boll = bt.indicators.BollingerBands(period,devfactor)

    def.next(self):
        if self.data.close < self.boll.lines.bot:
            self.order = self.buy()

class StFetcher(object):
    _STRATS = [BB, SmaCross]

    def __new__(cls, *args, **kwargs):
        idx = kwargs.pop('idx')

        obj = cls._STRATS[idx](*args, **kwargs)
        return obj

class VolumeWeightedAveragePrice(bt.Indicator):
    plotinfo = dict(subplot=False)

    params = (('period', 30), )

    alias = ('VWAP', 'VolumeWeightedAveragePrice',)
    lines = ('VWAP',)
    plotlines = dict(VWAP=dict(alpha=0.50, linestyle='-.', linewidth=2.0))



    def __init__(self):
        # Before super to ensure mixins (right-hand side in subclassing)
        # can see the assignment operation and operate on the line
        cumvol = bt.ind.SumN(self.data.volume, period = self.p.period)
        typprice = ((self.data.close + self.data.high + self.data.low)/3) * self.data.volume
        cumtypprice = bt.ind.SumN(typprice, period=self.p.period)
        self.lines[0] = cumtypprice / cumvol

        super(VolumeWeightedAveragePrice, self).__init__()
cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = bt.feeds.YahooFinanceData(dataname='resources\MAHABANK.NS.csv',
                                 fromdate=datetime(2020, 5, 6),
                                 todate=datetime(2021, 3, 23))
								 
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.optstrategy(VolumeWeightedAveragePrice, idx=[0, 1])
results = cerebro.run(maxcpus=args.maxcpus, optreturn=args.optreturn)
cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(SmaCross,pfast=10,pslow=40)  # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command