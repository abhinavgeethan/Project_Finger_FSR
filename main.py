import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

root="P_1"
idx='2'
emg_raw=pd.read_csv(f"{root}/unfiltered_emg{idx}.txt",header=None)
emg=pd.read_csv(f"{root}/emg{idx}.txt",header=None)
# gt=pd.read_csv(f"{root}/gt.txt",sep=' ',header=None)
stim=pd.read_csv(f"{root}/stim{idx}.txt",header=None)
# stim=pd.read_csv(f"{root}/stimulus.txt",sep=' ',header=None)
# print(emg.head())
time=pd.read_csv(f"{root}/timestamp{idx}.txt",header=None)
# labels=pd.read_csv(f"{root}/labels{idx}.txt",header=None)
# emg_raw=emg_raw[0:5927]
# emg=emg[0:5927]
# gt=gt[0:500]
# time=time[0:5927]
print(stim.shape)
plt.subplot(4,1,1)
plt.plot(time.iloc[:,1], emg_raw.iloc[:,1:11])
plt.subplot(4,1,2)
plt.plot(time.iloc[:,1], emg_raw.iloc[:,11:])
plt.subplot(4,1,3)
# plt.plot(time.iloc[:,1], gt.iloc[:,1:])
plt.plot(time.iloc[:,1], emg.iloc[:,1:11])
plt.subplot(4,1,4)
plt.plot(time.iloc[:,1], stim.iloc[:,1:7])
plt.show()
# plt.show()