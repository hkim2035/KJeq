import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from hampel import hampel
import glob 
import os

from multiprocessing import Process, Queue

def DataProcess(raw, df, dfX):
    
    outlier = hampel(dfX, 100, 3)
    dfX = dfX.drop(outlier)
    dfT = df.DateTime.drop(outlier)
    logfile = open("D:\\git\\KJeq\\hampel.log", 'a')
    logfile.write(f"No. of outlier in {dfX.name}: {len(outlier)}\n")
    logfile.close()
    exp_file = f"{os.path.basename(raw)[:-4]}_{dfX.name}.csv"
    dftemp = pd.concat([dfT, dfX], axis=1)
    dftemp.to_csv(exp_file)
    print(f"{os.path.basename(raw)[:-4]}_{dfX.name}... done")
    
    return

if __name__ == '__main__':

    all_files = sorted(glob.glob("D:\\git\\KJeq\\A*_all.csv"))

    for raw in all_files:
        df = pd.read_csv(raw, sep=',', header=0, skip_blank_lines=True)
        df.rename(columns={"MULTI_P1_REAL": "P1000", "MULTI_P2_REAL": "P500"}, inplace=True)
        df.rename(columns={"MULTI_T1_REAL": "T1000", "MULTI_T2_REAL": "T500"}, inplace=True)
        df['DateTime'] = pd.to_datetime(df.pop('Date')) + pd.to_timedelta(df.pop('Time'))
        #df.set_index('DateTime', inplace=True)
        logfile = open("D:\\git\\KJeq\\hampel.log", 'a')
        logfile.write(os.path.basename(raw))
        logfile.write(f"No. of data: {len(df)}\n")
        logfile.close()

        th1 = Process(target=DataProcess, args=(raw,df,df.P500))
        th2 = Process(target=DataProcess, args=(raw,df,df.P1000))
        th3 = Process(target=DataProcess, args=(raw,df,df.T500))
        th4 = Process(target=DataProcess, args=(raw,df,df.T1000))

        th1.start()
        th2.start()
        th3.start()
        th4.start()

        th1.join()
        th2.join()
        th3.join()
        th4.join()

    