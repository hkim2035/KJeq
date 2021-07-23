import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import numpy as np


df = pd.read_csv("D:\\git\\KJeq\\A1_2103_all_filtered.csv", sep=',', header=0, skip_blank_lines=True)

df['P500_time'] = pd.to_datetime(df['P500_time'])
df.set_index('P500_time', inplace=True)
ts = df['P500_signal']

plt.plot(ts)
plt.title('2021 March')
plt.ylabel('P500 signal')
plt.grid()
plt.show()


def check_stationarity(ts):
    dftest = adfuller(ts)
    adf = dftest[0]
    pvalue = dftest[1]
    critical_value = dftest[4]['5%']
    if (pvalue < 0.05) and (adf < critical_value):
        print('The series is stationary')
    else:
        print('The series is NOT stationary')

check_stationarity(ts)

ts_diff = ts.diff()
ts_diff.dropna(inplace=True)
check_stationarity(ts_diff)

plt.plot(ts_diff)
plt.title('Differenced Time Series')
plt.grid()
plt.show()



### Manual setting of model parameters and multi-step forecasting ###

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_pacf(ts_diff, lags =12)
plt.show()

print()
