from datetime import datetime

import backtrader as bt
import pandas as pd
from backtrader import cerebro
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .dataSources.gFinance.StockDataFeed import StockDataFeed, database_index
from .models import employee, knowledge
from .serializers import (UserSerializer, employeesSerializer,
                          knowledgeSerializer)
from .utility.File import File

# pd.set_option('display.max_rows', None)


stock_data_feed = StockDataFeed()
file = File()
knowledge_db = file.read(file_name='knowledge_db',
                         path=settings.BASE_DIR + '\\app\\resources\\', extension='json')
holdings = file.read(path='C:\\Users\\91880\\Downloads',
                     file_name='holdings', extension='csv')


class ExecutionTime():
    def __init__(self, method_name):
        self.method_name = method_name

    def start(self):
        self.start_time = datetime.now()

    def finish(self):
        self.finish_time = datetime.now()
        execution_time = (self.finish_time -
                          self.start_time).total_seconds() * 1000
        print('\nAPI: ' + self.method_name + ', Latency: ' +
              str(execution_time) + ' ms\n', flush=True)


class SMA(APIView):

    def get(self, request):
        execution_time = ExecutionTime('SMA.GET')
        execution_time.start()

        symbols_list = []
        for row in holdings:
            symbols_list.append(row[0])

        data = stock_data_feed.get_data(['HDFCBANK'])
        print(data, flush=True)
        for symbol in data:
            data_frame = data[symbol]
            window = 150
            data_frame['Sma50'] = data_frame.Close.rolling(
                window=window).mean().round(2).fillna(0)
            blob = data_frame[['Close', 'Sma50']]
            blob = blob[window-1:]

            count = 0
            prev = 0
            position = False
            total_profit_perc = 0
            total_loss_perc = 0
            trades = 0

            print('\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('| {0:>8}    |  {1:>8}    |  {2:>8}    |    {3:>8}    |'.format(
                'BUY', 'SELL', 'PnL', 'Pnl (%)'))
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            for (idx, row) in blob.iterrows():
                count += 1
                if count == 1:
                    prev = row.Sma50
                    continue

                if not position and prev < row.Sma50:
                    position = True
                    trades += 1
                    buy_price = row.Close
                    # print('BUY: {0}'.format(row.Close))

                if position and prev > row.Sma50:
                    position = False
                    pnl = round(row.Close - buy_price, 2)
                    pnl_perc = round(pnl/buy_price * 100.0)

                    if pnl_perc > 0:
                        total_profit_perc += pnl_perc
                    elif pnl_perc < 0:
                        total_loss_perc += pnl_perc

                    print('|{0:>10}   |  {1:>8}    |  {2:>8}    |  {3:>8} %    |'.format(
                        '{:.2f}'.format(buy_price), '{:.2f}'.format(row.Close), '{:.2f}'.format(pnl), '{:.2f}'.format(pnl_perc)))

                prev = row.Sma50

            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('\nSymbol: {0} \nTrades: {1} \nProfit Perc Sum: {2} \nLoss Perc Sum: {3} \nAvg Per Trade: {4} %'.format(
                symbol, trades, total_profit_perc, total_loss_perc, (total_profit_perc + total_loss_perc) / trades))

        execution_time.finish()
        # print(data_frame, flush=True)
        return Response(data_frame)


class highest(APIView):

    def get(self, request):
        start_time = datetime.now()

        # print("Calculating High ...", flush=True)
        # table = knowledge.objects.all()
        # result = knowledgeSerializer(table, many = True)
        # return Response(result.data)
        result = {}
        symbols_list = []

        for row in holdings:
            if not (row[0] in knowledge_db):
                symbols_list.append(row[0])

        # print(symbols_list, flush=True)

        data = stock_data_feed.get_data(symbols_list)
        print('Data downloaded...', flush=True)

        for symbol in data:
            try:
                blob = {}
                symbol_data = data[symbol]
                highest_price = -1
                hp_datetime = None
                hp_idx = 0
                for i in range(1, len(symbol_data)):
                    # print(hdfc_data[i], flush=True)
                    if float(symbol_data[i][4]) > float(highest_price):
                        highest_price = symbol_data[i][4]
                        hp_datetime = symbol_data[i][0]
                        hp_idx = i

                highest_price = float(highest_price)
                curr_price = float(symbol_data[len(symbol_data)-1][4])
                perc_change_from_high = round(
                    ((curr_price - highest_price) / highest_price) * 100, 2)
                number_of_days = len(symbol_data)-1-hp_idx

                blob['highest_price'] = highest_price
                blob['hp_datetime'] = hp_datetime
                blob['perc_change_from_high'] = perc_change_from_high
                blob['number_of_days'] = number_of_days
                result[symbol] = blob
            except Exception as e:
                print(e)

        finish_time = datetime.now()
        execution_time = (finish_time - start_time).total_seconds() * 1000
        print('Latency :' + str(execution_time) + ' ms', flush=True)
        return Response(knowledge_db)

    """
    def post(self):
        return 
    """


def index(request):
    data = StockDataFeed().get_data(['ITC'])
    for symbol in data:
        print(data[symbol][0], flush=True)
        print(data[symbol][1], flush=True)
        break
    return HttpResponse('Nice')


def calculate_all_symbols_avg():
    """ This function is to check what return you would get if you invest in all the companies. """
    start_time = datetime.now()
    # print('st : ' + str(start_time))
    stock_data_feed = StockDataFeed()

    symbols_list = []
    for symbol in database_index:
        symbols_list.append(symbol)

    new_symbols_list = symbols_list[0:10]

    data = stock_data_feed.get_data(new_symbols_list)

    for i in range(len(new_symbols_list)):
        # print(data[new_symbols_list[i]])
        if 1 == 1:
            x = True

    finish_time = datetime.now()
    execution_time = (finish_time - start_time).total_seconds() * 1000

    print('Latency :' + str(execution_time) + ' ms', flush=True)
    return data[new_symbols_list[0]]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class employeeList(APIView):

    def get(self, request):
        employees1 = employee.objects.all()
        result = employeesSerializer(employees1, many=True)
        return Response(result.data)

    """
    def post(self):
        return 
    """


def call_bt_test():
    cerebro = bt.Cerebro()
    data = bt.feeds.YahooFinanceData(dataname='MSFT',
                                     fromdate=datetime(2011, 1, 1),
                                     todate=datetime(2012, 12, 31))
    data = StockDataFeed().get_data(['ITC'])
    cerebro.adddata(data['ITC'])  # Add the data feed

    cerebro.addstrategy(SmaCross)  # Add the trading strategy
    cerebro.run()  # run it all
    cerebro.plot()  # and plot it with a single command


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


"""
balance = 0
invested = False
buy_price = 0
trades = 0
total_profit_perc = 0
total_loss_perc = 0

for (idx, row) in blob.iterrows():
    close_price = row.Close
    sma50 = row.Sma50

    if invested == False and close_price > sma50:
        buy_price = close_price
        trades += 1
        invested = True
    elif invested == True and close_price < sma50:
        pnl = close_price - buy_price
        pnl_perc = (pnl/buy_price) * 100

        if pnl > 0:
            total_profit_perc += pnl_perc
        elif pnl < 0:
            total_loss_perc += pnl_perc

        balance += pnl
        print('PnL: {0}, {1}%, BAL: {2}'.format(pnl, pnl_perc, balance))
        invested = False

print('Avg profit: {0}, Avg Loss: {1}'.format(total_profit_perc/trades, total_loss_perc/trades))
print('BALANCE: ' + str(balance))
"""
