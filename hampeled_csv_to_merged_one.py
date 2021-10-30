import glob
import os
import datetime as dt
import pandas as pd


def read_file(f):

    readf = pd.read_csv(f, header=0, sep=',', names=['time', 'data'])

    return readf


##### user input #####
target_sensor = ['P500', 'P1000', 'T500', 'T1000']
hole_ID = ["A1"]  # , "A2"]


for holeID in hole_ID:

    path = f"D:\\git\\data\\PT_{holeID}\\filtered"

    for sensor in target_sensor:

        all_files = sorted(
            glob.glob(os.path.join(path, f"*{holeID}_{sensor}.csv")))
        if len(all_files) > 0:
            raw = pd.concat([read_file(f) for f in all_files])
            # filter
            # dataset removed: x<=0, x>20,000(P) OR 100(T)

            raw.to_csv(f"{path}\\{holeID}_{sensor}_all.csv")
            print("OK.")
