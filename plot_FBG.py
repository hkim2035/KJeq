#!/usr/bin/env python

import calendar
import datetime
import sys
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from haversine import haversine

def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, skiprows=3, names=['Idx', 'Time','Mag', 'Depth', 'LAT', 'LON','Pos'], engine='python', encoding='utf-8')
    eqtlist.LAT = list(map(lambda x: float(x.split()[0]),eqtlist.LAT))
    eqtlist.LON = list(map(lambda x: float(x.split()[0]),eqtlist.LON))
    return eqtlist

def outlier_treatment(datacolumn):
    sorted(datacolumn)
    Q1, Q3 = np.percentile(datacolumn, [25, 75])
    IQR = Q3 - Q1
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)
    return lower_range, upper_range

eqtfile = "list_eq_20201001_20210531_KJ.csv"
rainfile = "rain2.csv"
# kigamfile = "D:\git\KJeq\A1_2021_05_17_23_40_21.csv"
kigamfile = "D:\git\KJeq\merge.csv"


monitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
                        'LON': [129.205945, 129.120528, 129.278389]},
                       index=["A1", "A2", "C2"])

# Get the total number of args passed
no_argv = len(sys.argv) 

if no_argv != 6:
     print ("Usage: plot_PT.py borehole_ID time_interval_for_removing_outliers 20##-##-## 20##-##-## mon or png")
     print ("Usage: When time_interval_for_removing_outliers is 0, data not filtered")
     print (" ")
     print ("hyunwoo.kim@kigam.re.kr")
     print ("2021.05")
     sys.exit() 

#holeID
holeID = sys.argv[1]

#filtering: No. of data in one section
no_data = int(sys.argv[2])

begin = datetime.datetime.strptime(sys.argv[3] +" 00:00:00", '%Y-%m-%d %H:%M:%S')
end = datetime.datetime.strptime(sys.argv[4] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
result_out = sys.argv[5]

if begin.month != end.month:
    end = end.replace(begin.year, begin.month, calendar.monthrange(end.year, end.month)[1],0,0,0)

sensorfile = f"PTsensor{holeID}_{(begin.year-2000):02d}{begin.month:02d}_all.csv"

df = pd.read_csv(sensorfile, header=0, sep=',')
df.rename(columns={"MULTI_P1_REAL": "P1000", "MULTI_P2_REAL": "P500"}, inplace=True)
df.rename(columns={"MULTI_T1_REAL": "T1000", "MULTI_T2_REAL": "T500"}, inplace=True)
df.Time = df.Date + " " + df.Time
df.Time = df.Time
df.Time = pd.to_datetime(df.Time, infer_datetime_format=True)
df = df[(df.Time >= begin) & (df.Time <= end)]

rain = pd.read_csv(rainfile, header=1, usecols=[1, 2], names=["Time","rain_mm"])
rain.Time = pd.to_datetime(rain.Time, infer_datetime_format=True)
rain = rain[(begin <= rain.Time) & (rain.Time < end)] 
rain = rain[np.isnan(rain.rain_mm)==False]

kigam = pd.read_csv(kigamfile, header=1, names=["d", "NPT","Time", "ddd","D01","D02","D03","D04","D05","D06","D07","D08","D09","D10","D11","D12","D13"])
kigam = kigam.dropna()

def change2(tt):
    return datetime.datetime.strptime(tt, '%Y-%m-%d %H:%M:%S')
kigam.Time = list(map(change2, kigam.Time))

kigam = kigam[(begin <= kigam.Time) & (kigam.Time < end)] 




# Outlier remove
def outlier_remove(time, signal, no_data):
    filtered_time = pd.Series(dtype='datetime64[ns]')
    filtered_signal = pd.Series(dtype='float')
    if (no_data != 0) & (len(signal) > 0):
        for ii in range(0, len(signal), no_data):
            ttime = time[ii:(ii + no_data)]
            tsignal = signal[ii:(ii + no_data)]
            lower, upper = outlier_treatment(tsignal)
            tsignal = tsignal[(tsignal>lower) & (tsignal<upper)]
            ttime = ttime[tsignal.index] 
            filtered_time = pd.concat([filtered_time, ttime])
            filtered_signal =pd.concat([filtered_signal, tsignal])
            
    return filtered_time, filtered_signal, len(signal)-len(filtered_signal), len(signal)

# print("Noise filtering...1/4")
# P500_time, P500_signal, removed_No, all_No = outlier_remove(df.Time, df.P500, no_data)
# print(f"Noise filtered...{removed_No}/{all_No}")
# print("Noise filtering...2/4")
# P1000_time, P1000_signal, removed_No, all_No = outlier_remove(df.Time, df.P1000, no_data)
# print(f"Noise filtered...{removed_No}/{all_No}")
# print("Noise filtering...3/4")
# T500_time, T500_signal, removed_No, all_No = outlier_remove(df.Time, df.T500, no_data)
# print(f"Noise filtered...{removed_No}/{all_No}")
# print("Noise filtering...4/4")
# T1000_time, T1000_signal, removed_No, all_No = outlier_remove(df.Time, df.T1000, no_data)
# print(f"Noise filtered...{removed_No}/{all_No}")

print("Graph generation...")
mode_type = 'lines' #'markers' #or 'lines'

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=False,
    vertical_spacing=0.08,
    row_heights = [0.46, 0.46],
    specs=[[{"type":"scatter"}], [{"type":"scatter"}]]
)





fig.add_trace(
    go.Scatter(
        x=kigam.Time,
        y=kigam.D01,
        mode=mode_type,
        name="FBG 000",
        marker_color='black',
        marker=dict(size=1)
    ),
    row=1, col=1)

fig.add_trace(
    go.Scatter(
        x=kigam.Time,
        y=kigam.D03,
        mode=mode_type,
        name="FBG 003",
        marker_color='black',
        marker=dict(size=1)
    ),
    row=1, col=1)

fig.add_trace(
    go.Scatter(
        x=kigam.Time,
        y=kigam.D05,
        mode=mode_type,
        name="FBG 005",
        marker_color='black',
        marker=dict(size=1)
    ),
    row=1, col=1)

fig.add_trace(
    go.Scatter(
        x=kigam.Time,
        y=kigam.D07,
        mode=mode_type,
        name="FBG 007",
        marker_color='black',
        marker=dict(size=1)
    ),
    row=1, col=1)

fig.add_trace(
    go.Scatter(
        x=kigam.Time,
        y=kigam.D09,
        mode=mode_type,
        name="FBG 009",
        marker_color='black',
        marker=dict(size=1)
    ),
    row=1, col=1)

#fig.layout.template = 'ggplot2' #seaborn'  vline not displayed

# fig.update_xaxes(range=[begin,end], tickformat="%d", tick0 = begin, dtick = 86400000, row=1, col=1)
# fig.update_xaxes(range=[begin,end], tickformat="%d", tick0 = begin, dtick = 86400000, row=2, col=1)

# begin_temp = math.floor(P500_signal.min()/10)*10
# if (begin_temp+40)<P500_signal.max():
#     end_temp = math.ceil(P500_signal.max()/10)*10
# else:
#     end_temp = begin_temp+40
# fig.update_yaxes(range=[begin_temp,end_temp], tickformat="%d", tick0 = begin_temp, dtick = (end_temp-begin_temp)/5, row=1, col=1)
# 
# begin_temp = math.floor(P1000_signal.min()/10)*10
# if (begin_temp+40)<P1000_signal.max():
#     end_temp = math.ceil(P1000_signal.max()/10)*10
# else:
#     end_temp = begin_temp+40
# fig.update_yaxes(range=[begin_temp,end_temp], tickformat="%d", tick0 = begin_temp, dtick = (end_temp-begin_temp)/5, row=2, col=1)


# fig.update_yaxes(title_text="P500 (kPa)", tickformat="d", row=1, col=1)
# fig.update_yaxes(title_text="P1000 (kPa)", tickformat="d", row=2, col=1)

fig.update_layout(
    autosize=False, width=1500, height=1000,
    font_family="NanumBarunGothic",
    font_color="black",
    title_font_family="NanumBarunGothic",
    title_font_color="black",
    legend_title_font_color="black",
    title={'text': f"FBG at Site {holeID} ({begin.year}.{begin.month:02d})", 'y':0.98, 'x':0.5, 'xanchor':'center', 'yanchor':'top'})

### earthquake line ###
eqlist = load_eq(eqtfile)
eqlist.Time = pd.to_datetime(eqlist.Time)
eqlist_this = eqlist[(begin <= eqlist.Time) & (eqlist.Time < end)]

for idx, eqvline in eqlist_this.iterrows():
    if eqvline.Mag >= 2:
        eqcolor = 'red'
    else:
        eqcolor = 'magenta'
    calDist = haversine((monitor.loc[holeID,:][0],monitor.loc[holeID,:][1]), (eqvline.LAT,eqvline.LON))
    if calDist < 5:
        dash ="solid"
    elif (calDist >=5) & (calDist <10):
        dash = "dash"
    else:
        dash = "dot"
    tY, tM, tD, tHH, tMM = eqvline.Time.year, eqvline.Time.month, eqvline.Time.day, eqvline.Time.hour, eqvline.Time.minute
    fig.add_vline(x=datetime.datetime(tY,tM,tD,tHH,tMM), line_color=eqcolor, line_dash = dash, row='all', col=1)
    # annotation_text=f"Mag.: {eqvline.Mag}", annotation_position="top left")
    #    line_width=1, line_dash="dash",


##########################

#fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.99, xanchor="right", x=1))
fig.update_layout(showlegend=False)

if result_out == "mon":
    fig.show()
elif result_out == "png":
    fname = f"D:\\FBG_{holeID}_{begin.year}_{begin.month:02d}"
    #fig.write_image(fname+'.png')
    fig.write_html(fname+'.html')
else:
    print("error.")
