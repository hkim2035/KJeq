import datetime
import folium
import io
from PIL import Image
import numpy as np
import pandas as pd

from folium.features import DivIcon
from haversine import haversine
import matplotlib.pyplot as plt

eqtfile = ".\\list_KJeq_160912_211010_r50km.csv"
#begin = "2016-09-12"
#end = "2017-11-14"
#begin = "2017-11-15"
#end = "2020-10-07"
begin = "2020-10-08"
end = "2021-10-10"

monitor = pd.DataFrame({'LAT': [35.746305, 35.741583, 35.730023],
                       'LON': [129.205945, 129.120528, 129.278389]},
                       index = ["Monitoring A1", "Monitoring A2", "Monitoring C2"])


#def load_wsm(wsmfile):
#    wsm = pd.read_csv(wsmfile)
#    wsmK= wsm[wsm.COUNTRY=="Korea - Republic of"].loc[:,['ID','LAT','LON','AZI','TYPE','DEPTH','REGIME']]
#    return wsmK

def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, encoding="utf-8")
    eqtlist.columns = ["index", "dTime","Mag", "Depth", "LAT", "LON","Pos"]
    eqtlist = eqtlist.dropna()
    eqtlist.dTime = pd.to_datetime(eqtlist.dTime)
    eqtlist.set_index(eqtlist.dTime, inplace=True)
    eqtlist.rename(columns = {'dTime' : 'Time'}, inplace = True)
          
    eqtlist.LAT = list(map(lambda x: float(x.split()[0]),eqtlist.LAT))
    eqtlist.LON = list(map(lambda x: float(x.split()[0]),eqtlist.LON))
    return eqtlist

eqlist = load_eq(eqtfile)
Maptype = 'OpenStreetMap'

m = folium.Map(location = [monitor.LAT.mean(), monitor.LON.mean()], zoom_start = 12, tiles = Maptype)
    
for index, mon in monitor.iterrows():
    folium.Marker([mon.LAT, mon.LON], popup=index, tooltip=index).add_to(m)

eqshow = eqlist[(eqlist.Time>=begin) & (eqlist.Time<=end)]

plt.rc('figure',figsize=(15,6))
plt.rc('font', size=12)
plt.rc('lines', markersize=4)

fig, ax = plt.subplots(1, 1)

ax.scatter(x=eqshow.index, y=eqshow['Mag'])
ax.axes.xaxis.grid(linestyle='--', linewidth=1)
ax.axes.yaxis.grid(linestyle='--', linewidth=1)
ax.set_ylim((0,6))
ax.set_xlabel("Time")
ax.set_ylabel("Magnitude")

plt.show()
plt.waitforbuttonpress()
plt.close()

if len(eqshow) != 0:
    i = 0
    eqresult = ""
    for idx, eq_each in eqshow.iterrows():
        i += 1
        eqdistA1 = haversine((monitor.LAT[0],monitor.LON[0]), (eq_each.LAT,eq_each.LON))
        eqdistA2 = haversine((monitor.LAT[1],monitor.LON[1]), (eq_each.LAT,eq_each.LON))
        print(i)
        eqtext = f'No.{i} {eq_each.Time} | Mag.:{eq_each.Mag} | Depth:{eq_each.Depth} km | Dist_A1:{eqdistA1:6.3f} km | Dist_A2:{eqdistA2:6.3f} km'
        xx = np.size(np.where(np.logical_and(eqshow.LAT==eq_each.LAT, eqshow.LON==eq_each.LON)))
        if xx > 0:
            folium.map.Marker([eq_each.LAT, eq_each.LON], 
                icon=DivIcon(icon_size=(300,36), icon_anchor=(0,0),
                html=f'<div style="font-size: 12pt"> <em> {xx} </em> </div>')).add_to(m)
        eqradius = int(xx)*5+45
        if eqradius < 50:
            eqradius = 50
        
        eqcolor = 'red'
        #if eq_each.Mag >= 2: 
        #    eqcolor = 'red'
        #    eqradius = 100
        #else:
        #    eqcolor = 'purple'
        #    eqradius = 100
        folium.Circle(
            location=[eq_each.LAT, eq_each.LON], radius=eqradius, color=eqcolor, fillcolor=eqcolor,
            z_index_offset=0, fill=True, tooltip=eqtext, popup=eqtext).add_to(m)
            
        
        
        
        
        

        eqresult = eqresult + eqtext + "\n"
    print(eqresult)


    # 2016.09.12 earthquake
    folium.Circle(
        location=[35.7666, 129.1879], radius=150, color='black', fillcolor='black',
        z_index_offset=0,
        fill=True, tooltip=f"2016-09-12 19:44:32 Mag.: 5.1 Depth: 15 km", popup=f"2016.09.12 19:44:32 Mag.: 5.1 Depth: 15 km").add_to(m)
    folium.Circle(
        location=[35.7610, 129.1878], radius=150, color='black', fillcolor='black',
        z_index_offset=0,
        fill=True, tooltip=f"2016-09-12 20:32:54 Mag.: 5.8 Depth: 15 km", popup=f"2016.09.12 20:32:54 Mag.: 5.8 Depth: 15 km").add_to(m)
    
    filename = f".\\KJeq_{begin}_{end}_R50km"
    m.save(filename + '.html')

    # A problem: png export
    #img_data = m._to_png(5)
    #img = Image.open(io.BytesIO(img_data))
    #img.save(filename + '.png')
    
    f = open(filename + '.txt','w')
    f.write(eqresult)
    f.close()
else:
    print("No earthquake detected.")