from googleServices.GoogleService import GoogleService
from googleServices.DriveService import DriveService
from googleServices.SheetsService import SheetsService
import googleServices
import time
from utility.Common import * 
from utility.File import *
import json

"""
# CREATE the SHEET with FORMULA for every SYMBOL and write the index(symbol, spreadSheetId)
def bootstrapStocksData(sheetService):
    symbolsList = getSymbols()
    index = {}

    try:
        for i in range(len(symbolsList)):
            time.sleep(8)
            print(str(i+1)+' ', end="")
            spreadSheetId = createSheet(sheetService)
            #writeSheet(sheetService, spreadSheetId, symbolsList[i])
    except:
        #writeIndex(index)
        print('Index Created till : '+i)

    index[symbolsList[i]] = spreadSheetId 
    writeIndex(index)
"""

def main():
    
    commonUtil = Common()
    fileUtil = File()

    googleService = GoogleService('utility/', 'secretKey.json')
    driveService = DriveService(googleService.get_drive_service())
    sheetsService = SheetsService(googleService.get_sheets_service())

    """
    reader = fileUtil.read_file(os.getcwd() + '/resources/', 'symbols.csv')
    #print(len(reader))

    all_files = driveService.get_all_files()
    spread_sheetids = []
    for i in range(len(all_files)):
        spread_sheetids.append(all_files[i]['id'])
        #print(spread_sheetids[i])

    i = 0
    database_index = {}
    for row in reader:
        symbol = row[0]
        spread_sheetid = spread_sheetids[i]
        print(symbol)
        print(spread_sheetid)
        database_index[symbol] = spread_sheetid
        i = i + 1

    fileUtil.write_file(database_index, os.getcwd() + '/resources/', 'database_index', 'json')

    #print(len(allfiles))
    for i in range(184):
        sheetsService.create_sheet()
        time.sleep(8)

    #print(len(driveService.get_all_files()))
    #commonUtil.sizeOf(reader)
    """

    with open(os.getcwd() + '/resources/'+'database_index.json') as f:
        data = json.load(f)

    try:
        see = False
        for symbol, spread_sheetid in data.items():
            #print(symbol)
            if symbol == 'CAPLIPOINT':
                see = True

            if see == True:
                sheetsService.write_sheet(spread_sheetid, symbol)
                print(symbol + ": success")
                time.sleep(10)

    except:
        print('broke at' + symbol)

if __name__ == "__main__":
    main()
