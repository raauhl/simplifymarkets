from googleServices.GoogleService import GoogleService
from googleServices.DriveService import DriveService
from googleServices.SheetsService import SheetsService
import googleServices
import time
from utility.Common import * 
from utility.File import *


# CREATE the SHEET with FORMULA for every SYMBOL and write the index(symbol, spreadSheetId)
def bootstrapStocksData(sheetService):
    try:
        for i in range(len(symbolsList)):
            time.sleep(8)
            print(str(i+1)+' ', end="")
            spreadSheetId = createSheet(sheetService)
            #writeSheet(sheetService, spreadSheetId, symbolsList[i])
    except:
        #writeIndex(index)
        print('Index Created till : '+i)


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
