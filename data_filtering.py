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

    # df = df.set_index(df.time)
    #
    # before_resampling = len(df)
    # if len(df.resample(rule=resampling_interval).first()) < before_resampling:
    #     df = df.resample(rule=resampling_interval).first()
    #     delta_no = before_resampling - len(df)
    # else:
    #     delta_no = 0
# 
    return filtered_time, filtered_signal, len(signal)-len(filtered_signal), len(signal) #, delta_no


if __name__== "__main__":

    ##### User input #####
    #holeID
    hole_ID = ["A1"]
#   #No. of data for removing outlier
    no_data = 100
    
    resampling_interval = '0s'
    
    for holeID in hole_ID:
    
        sensor_data = glob.glob(f".\\{holeID}_*_all.csv")
        check =0
        
        for sensor in sensor_data:
            
            print(sensor[2:len(sensor)-4])
            df = pd.read_csv(sensor, header=0, sep=',')
            
            df.rename(columns={"MULTI_P1_REAL": "P1000", "MULTI_P2_REAL": "P500"}, inplace=True)
            df.rename(columns={"MULTI_T1_REAL": "T1000", "MULTI_T2_REAL": "T500"}, inplace=True)
            df.Time = df.Date + " " + df.Time
            df.Time = pd.to_datetime(df.Time, infer_datetime_format=True)
    
            if resampling_interval == "0s":
                P500_time, P500_signal, removed_No, all_No = outlier_remove(df.Time, df.P500, no_data)
                print(f"P500 filtered..{removed_No}/{all_No}")
                P1000_time, P1000_signal, removed_No, all_No = outlier_remove(df.Time, df.P1000, no_data)
                print(f"P1000 filtered...{removed_No}/{all_No}")
                T500_time, T500_signal, removed_No, all_No = outlier_remove(df.Time, df.T500, no_data)
                print(f"T500 filtered...{removed_No}/{all_No}")
                T1000_time, T1000_signal, removed_No, all_No = outlier_remove(df.Time, df.T1000, no_data)
                print(f"T1000 filtered...{removed_No}/{all_No}")
            else:
                P500_time, P500_signal, removed_No, all_No, delta_No = outlier_remove(df.Time, df.P500, no_data)
                print(f"P500 filtered..{removed_No}/{all_No} & {delta_No} reduced")
                P1000_time, P1000_signal, removed_No, all_No, delta_No = outlier_remove(df.Time, df.P1000, no_data)
                print(f"P1000 filtered...{removed_No}/{all_No} & {delta_No} reduced")
                T500_time, T500_signal, removed_No, all_No, delta_No = outlier_remove(df.Time, df.T500, no_data)
                print(f"T500 filtered...{removed_No}/{all_No} & {delta_No} reduced")
                T1000_time, T1000_signal, removed_No, all_No, delta_No = outlier_remove(df.Time, df.T1000, no_data)
                print(f"T1000 filtered...{removed_No}/{all_No} & {delta_No} reduced")

            dfout = pd.DataFrame()
            dfout.insert(0, 'P500_time', np.transpose(P500_time))
            dfout.insert(1, 'P500_signal', np.transpose(P500_signal))
            dfout.insert(2, 'P1000_time', np.transpose(P1000_time))
            dfout.insert(3, 'P1000_signal', np.transpose(P1000_signal))
            dfout.insert(4, 'T500_time', np.transpose(T500_time))
            dfout.insert(5, 'T500_signal', np.transpose(T500_signal))
            dfout.insert(6, 'T1000_time', np.transpose(T1000_time))
            dfout.insert(7, 'T1000_signal', np.transpose(T1000_signal))
            
            check += 1
            print(f"filtered..{check}/{len(sensor_data)}\n")

            if resampling_interval == "0s":
                outfile = sensor[:len(sensor)-4]+"_filtered.csv"
            else:
                outfile = sensor[:len(sensor)-4]+"_filtered_resampled.csv"
                
            dfout.to_csv(outfile)