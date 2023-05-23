import requests
import key_info

from enumerations import Function 
from enumerations import OutputSize
from enumerations import Candle

import file_service
import constants

base_url = 'https://www.alphavantage.co/query?'


def get_data(function, symbol, outputsize, key):

    url = base_url + 'function={function}&symbol={symbol}&outputsize={outputsize}&apikey={apikey}'.format(
        function=function,
        symbol=symbol,
        outputsize=outputsize,
        apikey=key,
    )

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        file_service.create(data_json_blob=data, file_path=symbol+'_'+outputsize+'.json')
        return data
    else:
        print("Request failed with status code:", response.status_code)
        return None

def process_one():

    data = file_service.read('IVE_full.json')
    time_series = data[constants.TIME_SERIES_DAILY]
    
    
    for date, values in time_series.items():
        open_price = values[Candle.OPEN]
        high_price = values[Candle.HIGH]
        low_price = values[Candle.LOW]
        close_price = values[Candle.CLOSE]

    print(len(time_series.items()))


#data = get_data(Function.TIME_SERIES_DAILY_ADJUSTED, 'IVE', OutputSize.FULL, key_info.api_key)

process_one()