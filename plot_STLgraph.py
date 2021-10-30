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
from numpy import nan


def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, encoding="utf-8")
    eqtlist = eqtlist.dropna(axis=1)
    eqtlist.columns = ["Idx", "Time", "Mag", "Depth", "LAT", "LON", "Pos"]
    return eqtlist


def round(t, freq):
    freq = to_offset(freq)
    return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)


eqtfile = "c:\\Git\\KJeq\\list_KJeq_160912_211010_r50km.csv"

monitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
                        'LON': [129.205945, 129.120528, 129.278389]},
                       index=["A1", "A2", "C2"])


site = "A1"

# , '2106', '2010']:
for YYMM in ['2010', '2011', '2012', '2101', '2102', '2103', '2104', '2105']:

    df = pd.read_csv(
        f"C:\\Users\\hyunw\\OneDrive\\Data\\PTsensor\\{site}_{YYMM}_all_P500.csv", sep=',', header=0, skip_blank_lines=True)
    dfrain = pd.read_csv(f"C:\\Users\\hyunw\\OneDrive\\Data\\PTsensor\\KJ_rain_daily.csv",
                         sep=',', header=0, skip_blank_lines=True)
    dfrain['일시'] = pd.to_datetime(dfrain['일시'])
    dfrain.set_index('일시', inplace=True)

    YY = int(YYMM[:2])+2000
    MM = int(YYMM[2:])

    dfrain = dfrain[(dfrain.index.year == YY) & (dfrain.index.month == MM)]

    ts = df.iloc[:, [1, 2]]
    ts['DateTime'] = pd.to_datetime(ts['DateTime'])
    ts.set_index('DateTime', inplace=True)

    #tsR = ts.groupby(partial(round, freq="1T")).mean()
    tsR = ts.resample("1T").mean().dropna(axis=0)

    plt.rc('figure', figsize=(18, 16))
    plt.rc('font', size=12)
    plt.rc('lines', markersize=2)

    result = statsmodels.tsa.seasonal.seasonal_decompose(
        tsR, model='additive', period=1440)

    fig, axs = plt.subplots(5, 1, sharex=True)
    fig.subplots_adjust(hspace=0.1)
    fig.suptitle(f"Pressure at 500 m ({YY}-{MM}, {site})")

    axs[0].scatter(result.observed.index, result.observed, marker=",")
    axs[1].plot(result.trend)
    axs[2].plot(result.seasonal)
    axs[3].scatter(result.resid.index, result.resid, marker=",")
    axs[4].bar(dfrain.index, dfrain["일강수량(mm)"])
    if (axs[2].get_ylim()[0] >= -5) and (axs[2].get_ylim()[1] <= 5):
        axs[2].set_ylim((-5, 5))
    if (axs[3].get_ylim()[0] >= -20) and (axs[3].get_ylim()[1] <= 20):
        axs[3].set_ylim((-20, 20))
    if axs[4].get_ylim()[1] < 10:
        axs[4].set_ylim((0, 10))

    date_form = DateFormatter("%d")
    axs[3].xaxis.set_major_formatter(date_form)
    axs[4].set_xlabel("Time (day)")

    axs[0].set_ylabel("Observed")
    axs[1].set_ylabel("Trend")
    axs[2].set_ylabel("Seasonal")
    axs[3].set_ylabel("Residual")
    axs[4].set_ylabel("Rainfall (mm)")

    for i in [0, 1, 2, 3, 4]:
        axs[i].xaxis.grid(linestyle='--', linewidth=1)
        axs[i].yaxis.grid(linestyle='--', linewidth=1)
        axs[i].xaxis.set_ticks([datetime.datetime(YY, MM, dd)
                               for dd in range(1, calendar.monthrange(YY, MM)[1]+1, 1)])

    eqlist_this = eqlist[(eqlist.Time >= datetime.datetime(YY, MM, 1)) & (
        eqlist.Time <= datetime.datetime(YY, MM, calendar.monthrange(YY, MM)[1]))]

    for idx, eqvline in eqlist_this.iterrows():
        if eqvline.Mag >= 2:
            eqcolor = 'red'
            eqwidth = 6
        else:
            eqcolor = 'darkgrey'
            eqwidth = 4

        calDist = haversine(
            (monitor.loc[site, :][0], monitor.loc[site, :][1]), (eqvline.LAT, eqvline.LON))
        if calDist < 3:
            dash = "solid"
        # elif (calDist >=3) & (calDist <6):
        #    dash = "dashed"
        else:
            dash = "dotted"
        tY, tM, tD, tHH, tMM = eqvline.Time.year, eqvline.Time.month, eqvline.Time.day, eqvline.Time.hour, eqvline.Time.minute
        #axs[3].vlines(x=datetime.datetime(tY,tM,tD,tHH,tMM), ymin=0, ymax=1, colors = eqcolor, linestyles = dash)
        axs[3].axvline(x=eqvline.Time, color=eqcolor,
                       linewidth=eqwidth, linestyle=dash)

    # plt.show()
    plt.savefig(f".\\{YY}_{MM:2d}_{site}_P500_STL.png")
    # plt.waitforbuttonpress()
