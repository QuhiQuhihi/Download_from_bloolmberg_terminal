import os
import sys
import time
import datetime

import pandas as pd
import numpy as np

import blpapi
from xbbg import blp

# !pip install --index-url=https://bcms.bloomberg.com/pip/simple blpapi
# !pip install ruamel.yaml
# !pip install xbbg
# !pip install pyarrow
# from xbbg import blp

options = blpapi.SessionOptions()
options.setServerHost('localhost')
options.setServerPort(8194)
session = blpapi.Session(options)
session.start()

current_dir = os.getcwd()
data_dir = os.path.join(current_dir,"data")

_cusip_list = pd.read_csv("cusip_note_list.csv")
cusip_list = _cusip_list['cusip']

# _log_csv = pd.read_csv(os.path.join(current_dir, "log.csv"), index_col=False)

start = time.time()
k=0
num_ticker = 50
for i in range(int(len(cusip_list)/num_ticker)+1):
    _log_csv = pd.read_csv(os.path.join(current_dir, "log.csv"), index_col=False)
    target_list = cusip_list[(num_ticker*i) : (num_ticker*i)+num_ticker]
    
    data = blp.bdh(tickers= target_list, 
                   flds=['PX_CLEAN_MID', 'YLD_YTM_MID'],start_date='2003-01-01', end_date='2023-12-31')
    
    data.to_csv(os.path.join(data_dir,f"{i}.csv"))
    _log_csv.loc[len(_log_csv)] = {"completed" : target_list, "len": len(data)}
    
    print(round(100*i*num_ticker/53000,2), "  Completed (",i*num_ticker,") size is " , len(data))
    
    end = time.time()
    print("current run time is ", round((end-start),2), " seconds")
    
    mid = end
    _log_csv.to_csv(os.path.join(current_dir, "log.csv"), index=False)
    time.sleep(17)

print("logging for completed")