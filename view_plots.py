import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

root="P_2"
idx='3'

stim=pd.read_csv(f"data/{root}/stim{idx}.txt",header=None)
stim_activation=pd.read_csv(f"data/{root}/stim_activation{idx}.txt",header=None)
time=pd.read_csv(f"data/{root}/timestamp{idx}.txt",header=None)
emg=pd.read_csv(f"data/{root}/emg{idx}.txt",header=None)
raw_emg=pd.read_csv(f"data/{root}/unfiltered_emg{idx}.txt",header=None)

fsr_data=emg.iloc[:,1:11]
raw_fsr_data=raw_emg.iloc[:,1:11]
ffls_data=emg.iloc[:,11:]
good_stim=stim.iloc[:,1:7]
good_time=time.iloc[:,1]

# Plot FFLS Data
# for i in range(6):
#     plt.subplot(3,2,i+1)
#     plt.plot(good_time, ffls_data.iloc[:,i])

# Plot FFLS and Stim Data
# for i in range(6):
#     plt.subplot(3,2,i+1)
#     plt.plot(good_time, ffls_data.iloc[:,i])
#     plt.plot(good_time, good_stim.iloc[:,4-i])

# Plot FFLS, Stim & FSR Data
# for i in range(6):
#     plt.subplot(3,2,i+1)
#     plt.plot(good_time, ffls_data.iloc[:,i])
#     plt.plot(good_time, good_stim.iloc[:,4-i])
#     plt.plot(good_time, fsr_data)

# Plot FSR Data
# for i in range(10):
#     plt.subplot(5,2,i+1)
#     plt.plot(good_time, fsr_data.iloc[:,i])
#     plt.plot(good_time, raw_fsr_data.iloc[:,i])

# Plot Stimulations
# for i in range(6):
#     plt.subplot(3,2,i+1)
#     plt.plot(good_time, good_stim.iloc[:,4-i])

plt.show()