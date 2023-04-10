import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv(f"combined/emg_fsr_data.csv",header=0)
emg_fsr_time = [x for x in range(len(dataset))]
ffls_data = dataset.iloc[:,21:]
print(ffls_data.head())
print(ffls_data.max())
print(ffls_data.min())

def _normalize(data):
    return (data-np.min(data))/(np.max(data)-np.min(data))

def _standardize(array):
  mean = np.mean(array, axis=0)
  std = np.std(array, axis=0)
  array = (array - mean) / std
  return array

ffls_standardized = _standardize(ffls_data)
ffls_normalized = _normalize(ffls_data)
print(ffls_normalized.max())
print(ffls_normalized.min())
thresholds = [x-0.03 for x in ffls_normalized.mean()]

# plt.plot(emg_fsr_time,ffls_normalized)
for i in range(6):
    plt.subplot(3,2,i+1)
    plt.axhline(y=thresholds[i], color='r', linestyle='-') 
    plt.plot(emg_fsr_time,ffls_normalized.iloc[:,i])
    # plt.hist(ffls_normalized.iloc[:,i],50)
plt.show()