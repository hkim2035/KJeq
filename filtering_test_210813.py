import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from hampel import hampel

df = pd.read_csv("D:\\git\\KJeq\\A1_2104_all.csv", sep=',', header=0, skip_blank_lines=True)

df.rename(columns={"MULTI_P1_REAL": "P1000", "MULTI_P2_REAL": "P500"}, inplace=True)
df.rename(columns={"MULTI_T1_REAL": "T1000", "MULTI_T2_REAL": "T500"}, inplace=True)

df['DateTime'] = pd.to_datetime(df.pop('Date')) + pd.to_timedelta(df.pop('Time'))

outlier = hampel(df.P500, 100, 3)
df_filtered = df.drop(outlier)

print()


