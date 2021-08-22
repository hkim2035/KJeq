import pandas as pd
import matplotlib.pyplot  as plt 
import glob

if __name__=="__main__":
    
    for site in ["A1","A2"]:
        for item in ["P500","P1000","T500","T1000"]:
            
            fig, ax = plt.subplots(figsize=(8,3))
            ax.grid()
            ax.set_title(f"Monitoring site {site} - {item}", fontsize="16")
            ax.set_xlabel("Time", fontsize="15")
            if item[0] == "P":
                tmpstr = f"Hourly mean value of pressure at {item[1:]} m (KPa)"
            else:
                tmpstr = f"Hourly mean value of temperature at {item[1:]} m (Celsius)"
            ax.set_ylabel(tmpstr, fontsize="15")
            ax_c.set_ylabel("Standard deviation", fontsize="15")

            if item == "P500":
                ylim = [4000,6500]
            elif item == "P1000":
                ylim = [9000,11500]
            elif item == "T500":
                ylim = [25,45]
            else:
                ylim = [25,45]
            
            ax.set_ylim(ylim)

            if item[0] == "P":
                ax_c.set_ylim([0,150])
            else:
                ax_c.set_ylim([0,1])

            ax.plot(dfm.index, dfm[item], marker="o", ls="", markersize=1, color="black", zorder=0)
            ax_c.bar(dfs.index, dfs[item], color="blue", zorder=1, alpha=0.4)

            plt.savefig(f"plot_{site}_{item}.png", dpi=300)
            #plt.show()
            print("check")