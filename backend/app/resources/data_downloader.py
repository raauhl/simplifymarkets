
import csv
import historic_data

def bse_data_download(bse_sheet='symbols_bse.csv'):
    with open(bse_sheet) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
            
                bse = ".BO"
                ticker = row[2]+bse
                print(ticker)
            
                outfile = 'all_data_bse\{}.csv'.format(ticker)
                print(outfile)
                try:
                
                    historic_data.main(ticker,outfile)
                except:
                    f = open("failed_ticker_bse.txt", "a")
                    f.write(ticker)
                    f.close()

                line_count += 1
        print(f'Processed {line_count} lines.')
    
def nse_data_download(nse_sheet='symbols_nse.csv'):
    with open(nse_sheet) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
            
                bse = ".NS"
                ticker = row[0]+bse
                print(ticker)
            
                outfile = 'all_data_nse\{}.csv'.format(ticker)
                print(outfile)
                try:
                
                    historic_data.main(ticker,outfile)
                except:
                    f = open("failed_ticker_nse.txt", "a")
                    f.write(ticker)
                    f.close()
                line_count += 1
        print(f'Processed {line_count} lines.')
        
if __name__ == '__main__':
    nse_data_download()
    bse_data_download()