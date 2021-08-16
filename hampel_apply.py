import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from hampel import hampel
import glob 
import os

logfile = open("D:\\git\\KJeq\\hampel.log", 'w')
all_files = sorted(glob.glob("D:\\git\\KJeq\\A*_all.csv"))

for raw in all_files:
    df = pd.read_csv(raw, sep=',', header=0, skip_blank_lines=True)
    df.rename(columns={"MULTI_P1_REAL": "P1000", "MULTI_P2_REAL": "P500"}, inplace=True)
    df.rename(columns={"MULTI_T1_REAL": "T1000", "MULTI_T2_REAL": "T500"}, inplace=True)
    df['DateTime'] = pd.to_datetime(df.pop('Date')) + pd.to_timedelta(df.pop('Time'))
    #df.set_index('DateTime', inplace=True)
    logfile.write(os.path.basename(raw))
    logfile.write(f"No. of data: {len(df)}\n")
    
    for dfX in [df.P500, df.P1000, df.T500, df.T1000]:
        outlier = hampel(dfX, 100, 3)
        dfX = dfX.drop(outlier)
        dfT = df.DateTime.drop(outlier)
        logfile.write(f"No. of outlier in {dfX.name}: {len(outlier)}\n")
        exp_file = f"{os.path.basename(raw)[:-4]}_{dfX.name}.csv"
        dftemp = pd.concat([dfT, dfX], axis=1)
        dftemp.to_csv(exp_file)
        print(f"{os.path.basename(raw)[:-4]}_{dfX.name}... done")
        print()
    