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

import matplotlib, random

hex_colors_dic = {}
rgb_colors_dic = {}
hex_colors_only = []
for name, hex in matplotlib.colors.cnames.items():
    hex_colors_only.append(hex)
    hex_colors_dic[name] = hex
    rgb_colors_dic[name] = matplotlib.colors.to_rgb(hex)


def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, skiprows=2, names=['Idx', 'Time','Mag', 'Depth', 'LAT', 'LON','Pos'], engine='python', encoding='utf-8')
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

# Get the total number of args passed
no_argv = len(sys.argv) 

if no_argv != 7:
     print ("Usage: plot_FBG.py borehole_ID time_interval_for_removing_outliers 20##-##-## 20##-##-## mon or png source_file")
     print ("Usage: When time_interval_for_removing_outliers is 0, data not filtered")
     print (" ")
     print ("hyunwoo.kim@kigam.re.kr")
     print ("2021.05")
     sys.exit() 

# sensor file
sensorfile = sys.argv[6]

eqtfile = "list_KJeq.csv"
rainfile = "rain2.csv"

monitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
                        'LON': [129.205945, 129.120528, 129.278389]},
                       index=["A1", "A2", "C2"])

#holeID
holeID = sys.argv[1]

#filtering: No. of data in one section
no_data = int(sys.argv[2])

begin = datetime.datetime.strptime(sys.argv[3] +" 00:00:00", '%Y-%m-%d %H:%M:%S')
end = datetime.datetime.strptime(sys.argv[4] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
result_out = sys.argv[5]

if begin.month != end.month:
    end = end.replace(begin.year, begin.month, calendar.monthrange(end.year, end.month)[1],0,0,0)


df = pd.read_csv(sensorfile, header=1, names=["d","NPT","Time","dd","D01","D02","D03","D04","D05","D06","D07","D08","D09","D10","D11","D12","D13"], dtype={"D01":float,"D02":float,"D03":float,"D04":float,"D05":float,"D06":float,"D07":float,"D08":float,"D09":float,"D10":float,"D11":float,"D12":float,"D13":float})
df = df.dropna()
df = df[(df.D01>=0) & (df.D02>=0) & (df.D03>=0) & (df.D04>=0) & (df.D05>=0) & (df.D06>=0) & \
    (df.D07>=0) & (df.D08>=0) & (df.D09>=0) & (df.D10>=0) & (df.D11>=0) & (df.D12>=0) & (df.D13>=0)]

def change2(tt):
    return datetime.datetime.strptime(tt, '%Y-%m-%d %H:%M:%S')
df.Time = list(map(change2, df.Time))
df = df[(begin <= df.Time) & (df.Time < end)] 

print("Graph generation...")
mode_type = 'lines' #'markers' #or 'lines'

fig = make_subplots(rows=1, cols=1) #,
    # shared_xaxes=False,
    # vertical_spacing=0.08,
    # row_heights = [0.46, 0.46],
    # specs=[{"type":"scatter"}]  #, [{"type":"scatter"}]]
#)

for yy in [ df.D01, df.D02, df.D03, df.D04, df.D05, df.D06, df.D07, df.D08, df.D09, df.D10, df.D11, df.D12, df.D13]:
    fig.add_trace(
        go.Scattergl(
            x=df.Time,
            y=yy,
            mode=mode_type,
            name=yy.name,
            marker_color=random.choice(hex_colors_only),
            marker=dict(size=1)
        ),
        row=1, col=1)

fig.update_layout(
    autosize=False, width=1600, height=1200,
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

fig.update_layout(showlegend=True)

if result_out == "mon":
    fig.show()
elif result_out == "png":
    fname = f".\FBG_{holeID}_{begin.year}_{begin.month:02d}"
    fig.write_image(fname+'.png')
    fig.write_html(fname+'.html')
else:
    print("error.")
