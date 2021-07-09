import plotly.graph_objects as go
import numpy as np
import pandas as pd


def load_eq(eqtfile):
    eqtlist = pd.read_csv(eqtfile, skiprows=2, sep="\t", engine="python", encoding="euc-kr")
    eqtlist = eqtlist.dropna(axis=1)
    eqtlist.columns = ["Idx", "Time","Mag", "Depth", "LAT", "LON", "Pos"]
    eqtlist.Depth.astype('float')
    eqtlist.Depth = -eqtlist.Depth
    
    eqtlist.LAT = list(map(lambda x: float(x.split()[0]),eqtlist.LAT))
    eqtlist.LON = list(map(lambda x: float(x.split()[0]),eqtlist.LON))
    
    return eqtlist

eqtfile = ".\\list_KJeq.csv"

eqtlist = load_eq(eqtfile)

fig = go.Figure(data=[go.Scatter3d(
    x=eqtlist.LON,
    y=eqtlist.LAT,
    z=eqtlist.Depth,
    mode='markers',
    marker=dict(
        size=5,
        color=eqtlist.Mag,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)])

# tight layout
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
fig.update_yaxes(range = [1.25*np.max(eqtlist.LAT), 0.8*np.min(eqtlist.LAT)])
fig.update_yaxes(range = [1.25*np.max(eqtlist.LAT), 0.8*np.min(eqtlist.LAT)])
fig.show()


# Initialize the centroids
c1 = (129.2, 35.8, -12.0)
c2 = (129.4, 35.8, -12.0)
