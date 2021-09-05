import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime 

def dataplot(file, colnames):
    data = pd.read_csv(file, names=colnames)
    data = data[~data['Time'].str.contains("When", na=False, case=False)]

    data.Time = pd.to_datetime(data.Time)
    data = data.set_index(data.Time, drop=True)

    fig = plt.figure(figsize=(12,8))
    
    ax = fig.subplots(2,1, sharex=True)

    if len(data.columns)==5:
        ax[0].plot(data.index, data["P1"], color='blue', marker=".", ls="", lw=1)
        ax[0].plot(data.index, data["P2"], color='red', marker=".", ls="", lw=1)
        ax[0].grid(True)
        
        ax[1].plot(data.index, data["T1"], color='blue', marker=".", ls="", lw=1)
        ax[1].plot(data.index, data["T2"], color='red', marker=".", ls="", lw=1)
        ax[1].grid(True)
        
    else:
        ax[0].plot(data.index, data["P1"], color='blue', marker=".", ls="", lw=1)
        ax[0].grid(True)
        
        ax[01].plot(data.index, data["T1"], color='blue', marker=".", ls="", lw=1)
        ax[1].grid(True)
    
    fig.tight_layout()
    plt.show()

dataplot("E:\\data\\alldata_20210901.csv",["Time","P2","P1","T2","T1"])
plt.waitforbuttonpress()
plt.close()


dataplot("E:\\data\\alldata_20210830.csv",["Time","P1","T1"])
plt.waitforbuttonpress()
plt.close()

dataplot("E:\\data\\alldata_20210831.csv",["Time","P1","T1"])
plt.waitforbuttonpress()
plt.close()

dataplot("E:\\data\\alldata_20210901.csv",["Time","P2","P1","T2","T1"])
plt.waitforbuttonpress()
plt.close()


