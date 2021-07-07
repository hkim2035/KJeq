#!/usr/bin/env python
import numpy as np
import pandas as pd
import glob

def outlier_treatment(datacolumn):
    sorted(datacolumn)
    Q1, Q3 = np.percentile(datacolumn, [25, 75])
    IQR = Q3 - Q1
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)
    return lower_range, upper_range

# Outlier remove
def outlier_remove(time, signal, no_data):

    m = len(signal) // no_data
    tmpTime = [time[(no_data*ii):(no_data*(ii+1))] for ii in range(0,m,1)]
    tmpSignal = [signal[(no_data*ii):(no_data*(ii+1))] for ii in range(0,m,1)]
    tmpTime.append(time[(no_data*m):])
    tmpSignal.append(signal[(no_data*m):])

    filtered_time = pd.Series(dtype='datetime64[ns]')
    filtered_signal = pd.Series(dtype='float')

    for itime, isignal in zip(tmpTime, tmpSignal):
        lower, upper = outlier_treatment(isignal)
        isignal = isignal[(isignal>lower) & (isignal<upper)]
        itime = itime[isignal.index] 
        filtered_time = pd.concat([filtered_time, itime])
        filtered_signal =pd.concat([filtered_signal, isignal])


    df = pd.DataFrame()
    df.loc[:,'time'] = pd.Series(filtered_time)
    df.loc[:,'signal'] = pd.Series(filtered_signal)
    df = df.set_index(df.time)
    
    before_resampling = len(df)
    df = df.resample(rule=resampling_interval).first()
    delta_no = before_resampling - len(df)

    return filtered_time, filtered_signal, len(signal)-len(filtered_signal), len(signal), delta_no


if __name__== "__main__":

    ##### User input #####
    #holeID
    hole_ID = ["A1", "A2"]
#   #No. of data for removing outlier
    no_data = 100
    
    resampling_interval = '30s'
    
    for holeID in hole_ID:
    
        sensor_data = glob.glob(f"D:\\Data\\PTsensor\\{holeID}_*_all.csv")
        check =0
        
        for sensor in sensor_data:
            df = pd.read_csv(sensor, header=0, sep=',')
            
            df.rename(columns={"MULTI_P1_REAL": "P1000", "MULTI_P2_REAL": "P500"}, inplace=True)
            df.rename(columns={"MULTI_T1_REAL": "T1000", "MULTI_T2_REAL": "T500"}, inplace=True)
            df.Time = df.Date + " " + df.Time
            df.Time = pd.to_datetime(df.Time, infer_datetime_format=True)
    
            P500_time, P500_signal, removed_No, all_No, delta_No = outlier_remove(df.Time, df.P500, no_data)
            print(f"P500 filtered..{removed_No}/{all_No} & {delta_No} reduced")
            P1000_time, P1000_signal, removed_No, all_No, delta_No = outlier_remove(df.Time, df.P1000, no_data)
            print(f"P1000 filtered...{removed_No}/{all_No} & {delta_No} reduced")
            T500_time, T500_signal, removed_No, all_No, delta_No = outlier_remove(df.Time, df.T500, no_data)
            print(f"T500 filtered...{removed_No}/{all_No} & {delta_No} reduced")
            T1000_time, T1000_signal, removed_No, all_No, delta_No = outlier_remove(df.Time, df.T1000, no_data)
            print(f"T1000 filtered...{removed_No}/{all_No} & {delta_No} reduced")
          
            check += 1
            print(f"filtered..{check}/{len(sensor_data)}")

            outfile = sensor[:len(sensor)-4]+"_filtered_resampled.csv"

            df.to_csv(outfile)