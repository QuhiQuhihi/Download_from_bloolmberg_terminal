import os
import sys
import time
import datetime

import pandas as pd
import numpy as np

import xlsxwriter
import sqlite3


current_dir = os.getcwd()
data_dir = os.path.join(current_dir,"data")
result_dir = os.path.join(current_dir,"result")


database_name = "test_db_sqlite.db"
cusip_list_name = "cusip_note_list.csv"

# database_name = "test_db_sqlite.db"
# cusip_list_name = "test_list.csv"

# con = sqlite3.connect(database_name)
# cur = con.cursor()

cusip_file = pd.read_csv(os.path.join(current_dir, cusip_list_name))
cusip_list = cusip_file.iloc[:,0].tolist()

def download_write_excel(str_cusip):

    bbg_query = '=@BDH(B4,$B$5:$C$5,$B$1,$B$2,"Dir=V","CDR=5D","Days=A","QuoteType=P","Dts=S")'
    workbook = xlsxwriter.Workbook(os.path.join(data_dir, f"{str_cusip}_1.xlsx"))
    worksheet = workbook.add_worksheet()

    row, col = 0, 0

    worksheet.write(row, col, "StartDate")
    worksheet.write(row+1, col, "EndDate")
    
    worksheet.write(row, col+1, "1/1/2004")
    worksheet.write(row+1, col+1, "12/31/2013")

    worksheet.write(row+3, col+1, f"{str_cusip} Corp")

    worksheet.write(row+4, col, "Date")
    worksheet.write(row+4, col+1, "PX_CLEAN_MID")
    worksheet.write(row+4, col+2, "YLD_YTM_MID")

    worksheet.write(row+5, col, bbg_query)

    time.sleep(1)

    workbook.close()
    print(f"{str_cusip} period 1 completed")


    workbook = xlsxwriter.Workbook(os.path.join(data_dir, f"{str_cusip}_2.xlsx"))
    worksheet = workbook.add_worksheet()

    row, col = 0, 0

    worksheet.write(row, col, "StartDate")
    worksheet.write(row+1, col, "EndDate")
    
    worksheet.write(row, col+1, "1/1/2014")
    worksheet.write(row+1, col+1, "12/31/2023")

    worksheet.write(row+3, col+1, f"{str_cusip} Corp")

    worksheet.write(row+4, col, "Date")
    worksheet.write(row+4, col+1, "PX_CLEAN_MID")
    worksheet.write(row+4, col+2, "YLD_YTM_MID")

    worksheet.write(row+5, col, bbg_query)

    time.sleep(1)

    workbook.close()
    print(f"{str_cusip} period 2 completed")
    return 0                       


def execute_copy(str_cusip):
    current_time = datetime.datetime.now()

    data= pd.read_excel(os.path.join(data_dir, f"{str_cusip}_1.xlsx"), skiprows=4)
    bbg = data.copy(deep=False)

    bbg.loc[:,'cusip'] = str_cusip
    bbg.loc[:,'created_at'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
    bbg.loc[:,'modified_at'] = current_time.strftime("%Y-%m-%d %H:%M:%S")

    bbg.rename({'Date':'dates','PX_CLEAN_MID':'clean_mid', 'YLD_YTM_MID':'ytm_mid'})    

    bbg.to_csv(os.path.join(result_dir,f"{str_cusip}_1.csv"))
    
    print(f"completed {str_cusip}_1")


    data2= pd.read_excel(os.path.join(data_dir, f"{str_cusip}_2.xlsx"), skiprows=4)
    bbg2 = data2.copy(deep=False)

    bbg2.loc[:,'cusip'] = str_cusip
    bbg2.loc[:,'created_at'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
    bbg2.loc[:,'modified_at'] = current_time.strftime("%Y-%m-%d %H:%M:%S")

    bbg.rename({'Date':'dates','PX_CLEAN_MID':'clean_mid', 'YLD_YTM_MID':'ytm_mid'})    

    bbg.to_csv(os.path.join(result_dir,f"{str_cusip}_2.csv"))

    print(f"completed {str_cusip}_2")
    return 0


def log(str_cusip):
    log_csv = pd.read_csv(os.path.join(current_dir, "log.csv"))
    _log_csv = log_csv.copy(deep=True)
    _log_csv.loc[len(_log_csv)] = {"completed" : str_cusip}
    _log_csv.to_csv(os.path.join(current_dir, "log.csv"))
    print(f"logging for {str_cusip} completed")
    return 0


def main(cusip_list):
    for cusip in cusip_list:
        download_write_excel(cusip)
        execute_copy(cusip)
        log(cusip)