"""Usage: plot_PT_eacch_set.py borehole_ID 20##-##-## 20##-##-## mon or png
   - mon: only display
   - png: png and html
   - hyunwoo.kim@kigam.re.kr"""

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
    eqtlist = pd.read_csv(eqtfile, skiprows=2, sep="\t", engine="python", encoding="euc-kr")
    eqtlist = eqtlist.dropna(axis=1)
    eqtlist.columns = ["Idx", "Time","Mag", "Depth", "LAT", "LON","Pos"]
    
    eqtlist.LAT = list(map(lambda x: float(x.split()[0]),eqtlist.LAT))
    eqtlist.LON = list(map(lambda x: float(x.split()[0]),eqtlist.LON))
    return eqtlist

#============================
eqtfile = ".\\list_KJeq.csv"

mode_type = 'markers' #'markers' #or 'lines'

monitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
                        'LON': [129.205945, 129.120528, 129.278389]},
                       index=["A1", "A2", "C2"])
#============================


# Get the total number of args passed
no_argv = len(sys.argv) 

if no_argv != 5:
     print ("Usage: plot_PT_each_set.py borehole_ID 20##-##-## 20##-##-## mon or png")
     sys.exit() 

#holeID
holeID = sys.argv[1]

begin = datetime.datetime.strptime(sys.argv[2] +" 00:00:00", '%Y-%m-%d %H:%M:%S')
end = datetime.datetime.strptime(sys.argv[3] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
result_out = sys.argv[4]

if begin.month != end.month:
    end = end.replace(begin.year, begin.month, calendar.monthrange(end.year, end.month)[1],0,0,0)

sensorfile = f".\\{holeID}_{(begin.year-2000):02d}{begin.month:02d}_all_filtered.csv"

df = pd.read_csv(sensorfile, header=0, sep=',')
#df.rename(columns={"MULTI_P1_REAL": "P1000", "MULTI_P2_REAL": "P500"}, inplace=True)
#df.rename(columns={"MULTI_T1_REAL": "T1000", "MULTI_T2_REAL": "T500"}, inplace=True)
#df.Time = df.Date + " " + df.Time


print("Graph generation...")

fig = make_subplots(
    rows=4, cols=1,
    shared_xaxes=False,
    vertical_spacing=0.02,
    row_heights = [0.2, 0.2, 0.2, 0.2],
    specs=[[{"type":"scatter"}], [{"type":"scatter"}], [{"type":"scatter"}], [{"type":"scatter"}]]
)

fig.add_trace(
    go.Scatter(
        x=df.P500_time,
        y=df.P500_signal,
        mode=mode_type,
        name="Pressure (kPa) at 500 m",
        marker_color='black',
        marker=dict(size=1)
    ),
    row=1, col=1)

fig.add_trace(
    go.Scatter( 
        x=df.P1000_time,
        y=df.P1000_signal,
        mode=mode_type,
        name="Pressure (kPa) at 1000 m",
        marker_color='black',
        marker=dict(size=1)
    ),
    row=2, col=1)

fig.add_trace(
    go.Scatter(
        x=df.T500_time,
        y=df.T500_signal,
        mode=mode_type,
        name="Temperature (Cels.) at 500 m",
        marker_color='black',
        marker=dict(size=1)
    ),
    row=3, col=1)

fig.add_trace(
    go.Scatter(
        x=df.T1000_time,
        y=df.T1000_signal,
        mode=mode_type,
        name="Temperature (Cels.) at 1000 m",
        marker_color='black',
        marker=dict(size=1) 
    ),
    row=4, col=1)


#fig.layout.template = 'ggplot2' #seaborn'  vline not displayed

fig.update_xaxes(range=[begin,end], tickformat="%d", title_text="Time", tick0 = begin, dtick = 86400000, row=4, col=1)
fig.update_xaxes(range=[begin,end], tickformat="%d", tick0 = begin, dtick = 86400000, row=3, col=1)
fig.update_xaxes(range=[begin,end], tickformat="%d", tick0 = begin, dtick = 86400000, row=2, col=1)
fig.update_xaxes(range=[begin,end], tickformat="%d", tick0 = begin, dtick = 86400000, row=1, col=1)

begin_temp = math.floor(df.P500_signal.min()/100)*100
if (begin_temp+200)<df.P500_signal.max():
    end_temp = math.ceil(df.P500_signal.max()/100)*100
else:
    end_temp = begin_temp+200
fig.update_yaxes(range=[begin_temp,end_temp], tickformat="%d", tick0 = begin_temp, dtick = (end_temp-begin_temp)/5, row=1, col=1)

begin_temp = math.floor(df.P1000_signal.min()/10)*10
if (begin_temp+50)<df.P1000_signal.max():
    end_temp = math.ceil(df.P1000_signal.max()/10)*10
else:
    end_temp = begin_temp+50
fig.update_yaxes(range=[begin_temp,end_temp], tickformat="%d", tick0 = begin_temp, dtick = (end_temp-begin_temp)/5, row=2, col=1)


if holeID == 'A1':
    begin_temp = 27.5
else:
    begin_temp = math.floor(df.T500_signal.mean()*10)/10
fig.update_yaxes(range=[begin_temp-0.5,begin_temp+4.0], tickformat="%.1f", tick0 = begin_temp-0.5, dtick = 0.5, row=3, col=1)

if holeID == 'A1':
    begin_temp = 40.5
else:
    begin_temp = math.floor(df.T1000_signal.mean()*10)/10
fig.update_yaxes(range=[begin_temp-0.5,begin_temp+2.0], tickformat="%.1f", tick0 = begin_temp-0.5, dtick = 0.5, row=4, col=1)


fig.update_yaxes(title_text="P500 (kPa)", tickformat="d", row=1, col=1)
fig.update_yaxes(title_text="P1000 (kPa)", tickformat="d", row=2, col=1)
fig.update_yaxes(title_text="T500 (C)", tickformat=".1f", row=3, col=1)
fig.update_yaxes(title_text="T1000 (C)", tickformat=".1f", row=4, col=1)


fig.update_layout(
    autosize=False, width=810, height=1200,
    font_family="NanumBarunGothic",
    font_color="black",
    title_font_family="NanumBarunGothic",
    title_font_color="black",
    legend_title_font_color="black",
    title={'text': f"TELLUS Pressure & Temperature at Site {holeID} ({begin.year}.{begin.month:02d})", 'y':0.98, 'x':0.5, 'xanchor':'center', 'yanchor':'top'})

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
    
###########################

#fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.99, xanchor="right", x=1))
fig.update_layout(showlegend=False)

if result_out == "mon":
    fig.show()
elif result_out == "png":
    fname = f".\\PT_{holeID}_{(begin.year-2000):02d}{begin.month:02d}{begin.day:02d}-{end.month:02d}{end.day:02d}"
    fig.write_image(fname + '.png')
    fig.write_html(fname + '.html')
else:
    print("error.")
