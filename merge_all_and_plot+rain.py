import pandas as pd
import matplotlib.pyplot as plt
import glob


def merge_all(site, item):
    all_files = sorted(glob.glob(f".\{site}*{item}.csv"))
    df_rspm = pd.DataFrame()
    df_rsps = pd.DataFrame()
    for raw in all_files:
        df = pd.read_csv(raw, sep=',', header=0, skip_blank_lines=True)
        df = df.loc[:, ['DateTime', item]]
        df.DateTime = pd.to_datetime(df.DateTime)
        df.set_index(df.DateTime, drop=True, inplace=True)
        dfm = df.resample('1H').mean().dropna()
        dfs = df.resample('1H').std().dropna()
        df_rspm = pd.concat([df_rspm, dfm], axis=0)
        df_rsps = pd.concat([df_rsps, dfs], axis=0)
    return df_rspm, df_rsps


if __name__ == "__main__":

    dfrain = pd.read_csv('list_KJrain.csv')
    figr, axr = plt.subplots(figsize=(14, 3))
    axr.set_title(
        f"Daily rainfall (mm) in Gyeongju (2020.08-2021.09)", fontsize="12")
    axr.grid(axis='y', linestyle='--')
    axr.set_xlabel("Time", fontsize="12")
    axr.set_ylabel("Rainfall (mm)", fontsize="12")
    axr.set_ylim([0, 120])
    dfrain.time = pd.to_datetime(dfrain.time)
    axr.bar(dfrain.time, dfrain['rain_mm'], color="blue", zorder=1, alpha=1)
    plt.savefig(f"plot_rain.png", dpi=300)

    for site in ["A1", "A2"]:
        for item in ["P500", "P1000", "T500", "T1000"]:

            dfm, dfs = merge_all(site, item)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax_c = ax.twinx()
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
                ylim = [4000, 6500]
            elif item == "P1000":
                ylim = [9000, 11500]
            elif item == "T500":
                ylim = [25, 45]
            else:
                ylim = [25, 45]

            ax.set_ylim(ylim)

            if item[0] == "P":
                ax_c.set_ylim([0, 150])
            else:
                ax_c.set_ylim([0, 1])

            ax.plot(dfm.index, dfm[item], marker="o",
                    ls="", markersize=1, color="black", zorder=0)
            ax_c.bar(dfs.index, dfs[item], color="blue", zorder=1, alpha=0.4)

            plt.savefig(f"plot_{site}_{item}.png", dpi=300)
            # plt.show()
            print("check")
