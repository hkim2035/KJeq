import datetime
import folium
import io
from PIL import Image
import numpy as np
import pandas as pd

from folium.features import DivIcon
from haversine import haversine

# ======================
targetY = 2020
targetM = 10
# ======================


eqtfile = ".\\list_KJeq_210831.csv"

monitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
                       'LON': [129.205945, 129.120528, 129.278389]},
                       index=["Monitoring A1", "Monitoring A2", "Monitoring C2"])


def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, encoding="utf-8")
    eqtlist.columns = ["Time", "Mag", "Depth", "LAT", "LON", "Pos", "No"]
    #eqtlist = eqtlist.dropna()
    eqtlist.Time = pd.to_datetime(eqtlist.Time)
    eqtlist.set_index(eqtlist.Time, inplace=True)

    eqtlist.LAT = list(map(lambda x: float(x.split()[0]), eqtlist.LAT))
    eqtlist.LON = list(map(lambda x: float(x.split()[0]), eqtlist.LON))
    return eqtlist


eqlist = load_eq(eqtfile)

Maptype = 'OpenStreetMap'

m = folium.Map(location=[monitor.LAT.mean(),
               monitor.LON.mean()], zoom_start=13, tiles=Maptype)

print(f'Monitoring site: {len(monitor)} points')
print(
    f'Distance between A1 and A2: {haversine((monitor.LAT[0],monitor.LON[0]), (monitor.LAT[1],monitor.LON[1])):.1f} km')
print(
    f'Distance between A1 and C2: {haversine((monitor.LAT[0],monitor.LON[0]), (monitor.LAT[2],monitor.LON[2])):.1f} km')
print(
    f'Distance between A2 and C2: {haversine((monitor.LAT[1],monitor.LON[1]), (monitor.LAT[2],monitor.LON[2])):.1f} km')

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

filename = f'KJeq_from_{targetY:04d}-{targetM:02d}'
eqshow = eqlist

if len(eqshow) != 0:
    i = 0
    eqresult = ""
    for idx, eq_each in eqshow.iterrows():
        i += 1
        eqdistA1 = haversine(
            (monitor.LAT[0], monitor.LON[0]), (eq_each.LAT, eq_each.LON))
        eqdistA2 = haversine(
            (monitor.LAT[1], monitor.LON[1]), (eq_each.LAT, eq_each.LON))
        print(i)
        eqtext = f'No.{i} {eq_each.Time} | Mag.:{eq_each.Mag:4.1f} | Depth:{eq_each.Depth:00d} km | Dist_A1:{eqdistA1:6.2f} km | Dist_A2:{eqdistA2:6.2f} km'

        if eq_each.Mag >= 2:
            eqcolor = 'red'
            eqradius = 130
        else:
            eqcolor = 'yellow'
            eqradius = 100

        folium.Circle(
            location=[
                eq_each.LAT, eq_each.LON], radius=eqradius, color=eqcolor, fillcolor=eqcolor,
            z_index_offset=0, fill=True, tooltip=eqtext, popup=eqtext).add_to(m)

        folium.map.Marker([eq_each.LAT, eq_each.LON],
                          icon=DivIcon(icon_size=(300, 36), icon_anchor=(0, 0),
                                       html=f'<div style="font-size: 12pt"> <em> {eqshow.No[i-1]} <</em> </div>')).add_to(m)
        eqresult = eqresult + eqtext + "\n"
    print(eqresult)
    m.save(filename+'.html')

    # A problem: png export
    #img_data = m._to_png(5)
    #img = Image.open(io.BytesIO(img_data))
    #img.save(filename + '.png')

    f = open(filename + '.txt', 'w')
    f.write(eqresult)
    f.close()
else:
    print("No earthquake detected.")
