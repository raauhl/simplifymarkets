from ...googleServices.GoogleService import GoogleService
from ...resources import feed

import pandas as pd

sheets_service = GoogleService().get_sheets_service()

database_index = feed.get_symbols_info()

class StockDataFeed:
    """ Class to provide stock data. """

    def get_data(self, symbol_list):

        data = {}

        for symbol in symbol_list:
            sheet_id = database_index[symbol]
            stock_data = sheets_service.read_sheet(sheet_id)
            data_frame = pd.DataFrame(data=stock_data[1:], columns=stock_data[0], dtype=float)
            data_frame.fillna(0).round(2)
            data[symbol] = data_frame
            
        return data
