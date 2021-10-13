from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import pandas as pd

a = pd.read_csv("c:\\Users\\hyunw\\OneDrive\\Data\\PTsensor\\A1_2010_all_P500.csv")
raw = a['P500']
fs = 0.2 

f, t, Sxx = signal.spectrogram(raw, fs)
plt.pcolormesh(t, f, Sxx, shading="gouradu")



plt.show()
