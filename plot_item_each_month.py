import pandas as pd
import matplotlib.pyplot  as plt 
from datetime import datetime

def rain(datafile):
    df = pd.read_csv(datafile)
    dftmp = df.loc[:,["일시","일강수량(mm)"]]
    dftmp["일시"] = pd.to_datetime(dftmp["일시"])
    dftmp.set_index(dftmp["일시"], drop=True, inplace=True)
        
    return dftmp["일강수량(mm)"]

if __name__ == "__main__":

    fig, ax = plt.subplots((5,1), figsize=(8,11))
    ax.sharex()
    ax.grid()

    df_rain = rain(".\KJ_rain.csv")
    ax.bar(df_rain.index, df_rain, color="blue", zorder=1, alpha=0.4)

    for raw in ["A1_2010", "A1_2011", "A1_2012", "A1_2101", "A1_2102", "A1_2103", "A1_2104", "A1_2105", "A1_2106", "A2_2011", "A2_2012", "A2_2101", "A2_2102", "A2_2103", "A2_2104", "A2_2105", "A2_2106"]:

        year = 2000 + int(raw[3:5])    
        month = int(raw[-2:])
        this = f"{year}-{month}"
        
        df_rain = df_rain[this]

        for item in ["P500", "P1000", "T500", "T1000"]:

            df = pd.read_csv(f"{raw}_all_{item}.csv")
            dftmp = df.loc[:,["DateTime",item]]
            dftmp.DateTime = pd.to_datetime(dftmp.DateTime)
            dftmp.set_index(dftmp.DateTime, drop=True, inplace=True)

            plt.plot(dftmp[item],)
            print()            


    print()

#   for site in ["A1","A2"]:
#   f       
#   f       for item in ["P500","P1000","T500","T1000"]:
#   f           
#   f           all_files = sorted(glob.glob(f".\{site}*{item}.csv"))
#   f
#   f           for raw in all_files:
#   f               
#   f           fig, ax = plt.subplots(figsize=(8,3))
#   f           ax.grid()
#   f           ax.set_title(f"Monitoring site {site} - {item}", fontsize="16")
#   f           ax.set_xlabel("Time", fontsize="15")
#   f           if item[0] == "P":
#   f               tmpstr = f"Hourly mean value of pressure at {item[1:]} m (KPa)"
#   f           else:
#   f               tmpstr = f"Hourly mean value of temperature at {item[1:]} m (Celsius)"
#   f           ax.set_ylabel(tmpstr, fontsize="15")
#   f           ax_c.set_ylabel("Standard deviation", fontsize="15")
#   f
#   f           if item == "P500":
#   f               ylim = [4000,6500]
#   f           elif item == "P1000":
#   f               ylim = [9000,11500]
#   f           elif item == "T500":
#   f               ylim = [25,45]
#   f           else:
#   f               ylim = [25,45]
#   f           
#   f           ax.set_ylim(ylim)
#   f
#   f           if item[0] == "P":
#   f               ax_c.set_ylim([0,150])
#   f           else:
#   f               ax_c.set_ylim([0,1])
#   f
#   f           ax.plot(dfm.index, dfm[item], marker="o", ls="", markersize=1, color="black", zorder=0)
#   f           ax_c.bar(dfs.index, dfs[item], color="blue", zorder=1, alpha=0.4)
#   f
#   f           plt.savefig(f"plot_{site}_{item}.png", dpi=300)
#   f           #plt.show()
#   f           print("check")