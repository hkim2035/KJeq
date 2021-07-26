import calendar
import datetime
from functools import partial
from matplotlib import colors

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.tsa.seasonal
from haversine import haversine
from matplotlib.dates import DateFormatter
from numpy.core.function_base import linspace
from pandas.tseries.frequencies import to_offset


def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, skiprows=2, sep="\t", engine="python", encoding="euc-kr")
    eqtlist = eqtlist.dropna(axis=1)
    eqtlist.columns = ["Idx", "Time","Mag", "Depth", "LAT", "LON","Pos"]
    
    eqtlist.LAT = list(map(lambda x: float(x.split()[0]),eqtlist.LAT))
    eqtlist.LON = list(map(lambda x: float(x.split()[0]),eqtlist.LON))
    return eqtlist

def round(t, freq):
    freq = to_offset(freq)
    return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)

eqtfile = ".\\list_KJeq.csv"

monitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
                        'LON': [129.205945, 129.120528, 129.278389]},
                       index=["A1", "A2", "C2"])


site = "A2" #"A1"

for YYMM in ['2011', '2012', '2101', '2102', '2103', '2104', '2105', '2106', '2010']:

    df = pd.read_csv(f"D:\\git\\KJeq\\{site}_{YYMM}_all_filtered.csv", sep=',', header=0, skip_blank_lines=True)

    YY = int(YYMM[:2])+2000
    MM = int(YYMM[2:])

    ts = df.iloc[:,[1,2]]
    ts['P500_time'] = pd.to_datetime(ts['P500_time'])
    ts.set_index('P500_time', inplace=True)

    tsR = ts['P500_signal'].groupby(partial(round, freq="1T")).mean()

    plt.rc('figure',figsize=(18,14))
    plt.rc('font', size=12)
    plt.rc('lines', markersize=2)

    result = statsmodels.tsa.seasonal.seasonal_decompose(tsR, model='additive', period=1440)

    fig, axs = plt.subplots(4, 1, sharex=True)
    fig.subplots_adjust(hspace=0.1)
    fig.suptitle(f"Pressure at 500 m ({YY}-{MM}, {site})")

    axs[0].scatter(result.observed.index,result.observed, marker=",")
    axs[1].plot(result.trend)
    axs[2].plot(result.seasonal)
    axs[3].scatter(result.resid.index,result.resid, marker=",")

    date_form = DateFormatter("%d")
    axs[3].xaxis.set_major_formatter(date_form)
    axs[3].set_xlabel("Time")

    axs[0].set_ylabel("Observed")
    axs[1].set_ylabel("Trend")
    axs[2].set_ylabel("Seasonal")
    axs[3].set_ylabel("Residual")

    for i in [0, 1, 2, 3]:
        axs[i].xaxis.grid(linestyle='--', linewidth=1) 
        axs[i].yaxis.grid(linestyle='--', linewidth=1)
        axs[i].xaxis.set_ticks([datetime.datetime(YY,MM,dd) for dd in range(1,calendar.monthrange(YY,MM)[1]+1,1)])

    
    eqlist = load_eq(eqtfile)
    eqlist.Time = pd.to_datetime(eqlist.Time)
    eqlist_this = eqlist[(eqlist.Time >= datetime.datetime(YY,MM,1)) & (eqlist.Time <= datetime.datetime(YY,MM,calendar.monthrange(YY,MM)[1]))]

    for idx, eqvline in eqlist_this.iterrows():
        if eqvline.Mag >= 2:
            eqcolor = 'red'
        else:
            eqcolor = 'magenta'
        calDist = haversine((monitor.loc[site,:][0],monitor.loc[site,:][1]), (eqvline.LAT,eqvline.LON))
        if calDist < 3:
            dash ="solid"
        elif (calDist >=3) & (calDist <6):
            dash = "dashed"
        else:
            dash = "dotted"
        tY, tM, tD, tHH, tMM = eqvline.Time.year, eqvline.Time.month, eqvline.Time.day, eqvline.Time.hour, eqvline.Time.minute
        #axs[3].vlines(x=datetime.datetime(tY,tM,tD,tHH,tMM), ymin=0, ymax=1, colors = eqcolor, linestyles = dash)
        axs[3].axvline(x = eqvline.Time, color = eqcolor, linestyle = dash)

    # plt.show()
    plt.savefig(f".\\{YY}_{MM}_{site}_P500_STL.png")
    # plt.waitforbuttonpress()
