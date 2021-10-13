import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob 
import os


for type in ['P500', 'P1000', 'T500', 'T1000']:
    
    rf = open(f"c:\\git\\KJeq\\range_{type}.csv", 'w')
    rf.write(f"Site,YYMM,{type}mean,{type}std,{type}max,{type}min\n")

    all_files = sorted(glob.glob(f"c:\\users\\hyunw\\OneDrive\\Data\\PTsensor\\A*_all_{type}.csv"))

    for raw in all_files:
        df = pd.read_csv(raw, sep=',', header=0, skip_blank_lines=True)
        df.set_index(df.DateTime, inplace=True)
        info = f"{os.path.basename(raw)[0:2]},{os.path.basename(raw)[3:7]},"
        info += f"{df[type].mean():.3f},{df[type].std():.3f},{df[type].max():.3f},{df[type].min():.3f}\n"
        rf.write(info)
    
    rf.close()