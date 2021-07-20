import datetime
import folium
import io
from PIL import Image
import numpy as np
import pandas as pd
from folium.features import DivIcon
from folium.plugins import HeatMap

from haversine import haversine


eqtfile = ".\\list_KJeq210719.csv"

monitor = pd.DataFrame({'LAT': [35.746305, 35.741583],
                        'LON': [129.205945, 129.120528]},
                        index = ["Monitoring A1", "Monitoring A2"])
#onitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
#                       'LON': [129.205945, 129.120528, 129.278389]},
#                       index = ["Monitoring A1", "Monitoring A2", "Monitoring C2"])


def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, skiprows=1, sep=",", engine="python", encoding="cp437")
    eqtlist = eqtlist.dropna(axis=1)
    eqtlist.columns = ["Time","Mag", "Depth", "LAT", "LON","Pos"]
    
    eqtlist.LAT = list(map(lambda x: float(x.split()[0]),eqtlist.LAT))
    eqtlist.LON = list(map(lambda x: float(x.split()[0]),eqtlist.LON))
    return eqtlist

eqlist = load_eq(eqtfile)

Maptype = 'OpenStreetMap'

m = folium.Map(location = [monitor.LAT.mean(), monitor.LON.mean()], zoom_start = 13, tiles = Maptype)
    
print(f'Monitoring site: {len(monitor)} points')
print(f'Distance between A1 and A2: {haversine((monitor.LAT[0],monitor.LON[0]), (monitor.LAT[1],monitor.LON[1])):.3f} km')
    
for index, mon in monitor.iterrows():
    folium.Marker([mon.LAT, mon.LON], popup=index, tooltip=index).add_to(m)

# 2016.09.12 earthquake
folium.Circle(
    location=[35.7666, 129.1879], radius=150, color='black', fillcolor='black',
    z_index_offset=0,
    fill=True, tooltip=f"2016-09-12 19:44:32 Mag.: 5.1 Depth: 15 km", popup=f"2016.09.12 19:44:32 Mag.: 5.1 Depth: 15 km").add_to(m)
folium.Circle(
    location=[35.7610, 129.1878], radius=150, color='black', fillcolor='black',
    z_index_offset=0,
    fill=True, tooltip=f"2016-09-12 20:32:54 Mag.: 5.8 Depth: 15 km", popup=f"2016.09.12 20:32:54 Mag.: 5.8 Depth: 15 km").add_to(m)

eqlist.Time = pd.to_datetime(eqlist.Time)

eqshow = eqlist

eqshow = eqshow.sort_values(by=['Time'], axis=0)

if len(eqshow) != 0:
    i = 0
    eqresult = ""
    for idx, eq_each in eqshow.iterrows():
        i += 1
        eqdistA1 = haversine((monitor.LAT[0],monitor.LON[0]), (eq_each.LAT,eq_each.LON))
        eqdistA2 = haversine((monitor.LAT[1],monitor.LON[1]), (eq_each.LAT,eq_each.LON))
        print(i)
        eqtext = f'No.{i} {eq_each.Time} | Mag.:{eq_each.Mag} | Depth:{eq_each.Depth} km | Dist_A1:{eqdistA1:6.3f} km | Dist_A2:{eqdistA2:6.3f} km'
        eqresult = eqresult + eqtext + "\n"
        
    print(eqresult)
    

    HeatMap(zip(eqshow.LAT, eqshow.LON), min_opacity=0.5, radius=3, blur=1, max_zoom=1, color='red').add_to(m)

else:
    print("No earthquake detected.")

m.save("D:\\tempH.html")
