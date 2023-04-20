import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv(f"combined/emg_fsr_data.csv",header=0)
emg_fsr_time = [x for x in range(len(dataset))]
ffls_data = dataset.iloc[:,21:]

def _normalize(data):
    return (data-data.min())/(data.max()-data.min())

def _standardize(array):
  mean = np.mean(array, axis=0)
  std = np.std(array, axis=0)
  array = (array - mean) / std
  return array

def press_locations(ffls_data,finger):
  ffls_data.columns=['Fing1','Fing2','Fing3','Fing4','Fing5','Fing6'] # Renaming Columns
  ffls_standardized = _standardize(ffls_data)
  ffls_normalized = _normalize(ffls_standardized)
  ffls_normalized['key']=dataset.iloc[:,0]
  ffls_normalized=ffls_normalized[['key','Fing1','Fing2','Fing3','Fing4','Fing5','Fing6']]
  thresholds = [x-0.03 for x in ffls_normalized.mean()]
  indices=[]
  idx_list=np.where(ffls_normalized[f'Fing{finger}']<thresholds[finger])[0]
  for idx in idx_list:
    indices.append(idx)
  return indices

def make_moving_avg(ffls_data):
    mov_avg_ffls = ffls_data.rolling(3).mean()
    mov_avg_ffls.fillna(0.0,inplace=True)
    return mov_avg_ffls

def make_thresholds(data):
    return [x-0.03 for x in data.mean()]

# Show FFLS Normalized Thresholds
# ffls_normalized = _normalize(_standardize(ffls_data))
# thresholds = make_thresholds(ffls_normalized)
# for i in range(6):
#     plt.subplot(3,2,i+1)
#     plt.axhline(y=thresholds[i], color='r', linestyle='-')
#     plt.plot(emg_fsr_time,ffls_normalized.iloc[:,i])
#     plt.title(f"Finger {i+1}")
#     plt.legend(['Threshold','Force'])

# Show Finger Press Locations
mov_avg_ffls = make_moving_avg(ffls_data)
plt.plot(emg_fsr_time,mov_avg_ffls)
colors=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
for i in range(1,7):
  for idx in press_locations(mov_avg_ffls,i):
    plt.axvline(x=idx,linestyle='-',color=colors[i],alpha=0.01)
plt.show()