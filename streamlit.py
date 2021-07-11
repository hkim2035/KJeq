import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
from haversine import haversine

# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from datetime import datetime, timedelta, date, time
import math
# from modeler.core import Core

### Based on https://github.com/gregoirejan/met/blob/main/metapp.py ###


st.set_page_config(layout="wide")

# hide_streamlit_style = """
#             <style>
#             footer:after {
#                 content:'by https://gregoirejan.github.io / Using frost.met.no API'; 
#                 visibility: visible;
#                 display: block;
#                 position: relative;
#                 #background-color: red;
#                 padding: 5px;
#                 top: 2px;
#             }
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

##############################################################################################################################################
st.sidebar.title('TELLUS PT Monitoring')

wsmfile = ".\\wsmK.csv"
eqtfile = ".\\list_KJeq.csv"
obsfile = ".\\eq_obs3.csv"

monitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
                       'LON': [129.205945, 129.120528, 129.278389]},
                       index = ["Monitoring A1", "Monitoring A2", "Monitoring C2"])

@st.cache
def load_wsm(wsmfile):
    wsm = pd.read_csv(wsmfile)
    wsmK= wsm[wsm.COUNTRY=="Korea - Republic of"].loc[:,['ID','LAT','LON','AZI','TYPE','DEPTH','REGIME']]
    return wsmK

@st.cache
def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, skiprows=2, sep="\t", engine="python", encoding="euc-kr")
    eqtlist = eqtlist.dropna(axis=1)
    eqtlist.columns = ["Idx", "Time","Mag", "Depth", "LAT", "LON","Pos"]

    
    eqtlist.LAT = list(map(lambda x: float(x.split()[0]),eqtlist.LAT))
    eqtlist.LON = list(map(lambda x: float(x.split()[0]),eqtlist.LON))

    return eqtlist

@st.cache
def load_obs(obsfile):
    obslist = pd.read_csv(obsfile, skiprows=1, names=['Code', 'LAT', 'LON'], 
                          engine='python', encoding='utf-8')
    return obslist

wsmK = load_wsm(wsmfile)
eqlist = load_eq(eqtfile)
obslist = load_obs(obsfile)

Maptype = 'OpenStreetMap'

m = folium.Map(location = [monitor.LAT.mean(), monitor.LON.mean()], zoom_start = 12, tiles = Maptype)
    
for index, mon in monitor.iterrows():
    folium.Marker([mon.LAT, mon.LON], popup=index, tooltip=index).add_to(m)

folium_static(m)
st.write(f'Monitoring site: {len(monitor)} points')
st.write(f'Distance between A1-A2: {haversine((monitor.LAT[0],monitor.LON[0]), (monitor.LAT[1],monitor.LON[1])):.2f} km, \
    A1-C1: {haversine((monitor.LAT[0],monitor.LON[0]), (monitor.LAT[2],monitor.LON[2])):.2f} km')

st.sidebar.opt

