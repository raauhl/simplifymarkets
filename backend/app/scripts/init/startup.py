from googleServices.GoogleService import GoogleService
from googleServices.DriveService import DriveService
from googleServices.SheetsService import SheetsService
import googleServices
import time
from utility.Common import * 
from utility.File import *
import json


def main():
    """
    commonUtil = Common()
    fileUtil = File()

    googleService = GoogleService('utility/', 'secretKey.json')
    driveService = DriveService(googleService.get_drive_service())
    sheetsService = SheetsService(googleService.get_sheets_service())

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


if __name__ == "__main__":
    main()

    """
    try:
        see = False
        for symbol, spread_sheetid in data.items():
            #print(symbol)
            #if symbol == 'MARUTI':
                #see = True
            data = sheetsService.read_sheet(spread_sheetid)
            commonUtil.sizeOf(data)
            #print(data)

            break

            if see == True:
                sheetsService.write_sheet(spread_sheetid, symbol)
                print(symbol + ": success")
                time.sleep(10)
                
    except Exception as e: print(e)
    """