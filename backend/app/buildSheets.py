from googleServices.GoogleService import GoogleService
from googleServices.DriveService import DriveService
from googleServices.SheetsService import SheetsService
import googleServices
import time
from utility.Common import * 
from utility.File import *
import json

def main():
    
    commonUtil = Common()
    fileUtil = File()

    googleService = GoogleService('utility/', 'secretKey.json')
    driveService = DriveService(googleService.get_drive_service())
    sheetsService = SheetsService(googleService.get_sheets_service())


if __name__ == "__main__":
    main()
