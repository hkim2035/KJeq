"""Code for merging daily PT sensor data (CSV files) to one monthly data.

   - 'input_path', 'hole_ID' and 'target_month' should be given in the code.
   - Data <= 0 or >=20000 (Pressure) or >=100 (Temperature) are removed."""

import glob
import os
import datetime as dt
import pandas as pd

##### user input #####
input_path = "d:\\data\\PTsensor\\"
target_month = ['2106']     #yymm
hole_ID = ["A1", "A2"]

def read_file(f):
    try:
        readf = pd.read_csv(f, header='infer', sep=',', usecols=['Date','Time','MULTI_P1_REAL','MULTI_T1_REAL','MULTI_P2_REAL','MULTI_T2_REAL'])
    except:
        readf = pd.read_csv(f, header=0, sep=',', names=['Time','MULTI_P1_REAL','MULTI_T1_REAL','MULTI_P2_REAL','MULTI_T2_REAL'])
        A = pd.to_datetime(readf.Time)
        D = pd.DataFrame(list(map(lambda X: X.date().strftime("%Y/%m/%d"), A)))
        readf.insert(0,'Date',D)
        readf.Time = pd.DataFrame(list(map(lambda X: X.time().strftime("%H:%M:%S"), A)))

    return readf

for holeID in hole_ID:
    input_path1 = input_path + holeID + "\\MULTI_1"
    output_path = input_path
    for month in target_month: 
        all_files = sorted(glob.glob(os.path.join(input_path1, month + "*.csv")))
        if len(all_files) > 0:
            raw = pd.concat([read_file(f) for f in all_files])
            #filter
            #dataset removed: x<=0, x>20,000(P) OR 100(T)
            raw = raw[(raw.MULTI_P1_REAL > 0) & (raw.MULTI_P1_REAL < 20000)]
            raw = raw[(raw.MULTI_P2_REAL > 0) & (raw.MULTI_P2_REAL < 20000)]
            raw = raw[(raw.MULTI_T1_REAL > 0) & (raw.MULTI_T1_REAL <= 100)]
            raw = raw[(raw.MULTI_T2_REAL > 0) & (raw.MULTI_T2_REAL <= 100)]
            raw.to_csv(output_path + holeID + "_" + month +"_all.csv")
            print("OK.")