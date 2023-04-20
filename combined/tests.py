import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv(f"combined/emg_fsr_data.csv",header=0)
emg_fsr_time = [x for x in range(len(dataset))]
ffls_data = dataset.iloc[:,21:]
# print(ffls_data.head())
# print(ffls_data.max())
# print(ffls_data.min())

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
  
  # Copying Key column to FFLS Data
  ffls_normalized['key']=dataset.iloc[:,0]
  # Reordering columns
  ffls_normalized=ffls_normalized[['key','Fing1','Fing2','Fing3','Fing4','Fing5','Fing6']]
  # Calculate Thresholds
  thresholds = [x-0.03 for x in ffls_normalized.mean()]
  
  indices=[]
  # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-where-column-matches-certain-value
  # Find where Finger is pressed
  idx_list=np.where(ffls_normalized[f'Fing{finger}']<thresholds[finger])[0]
  for idx in idx_list:
    indices.append(idx)
  return indices


mov_avg_ffls = ffls_data.rolling(3).mean()
mov_avg_ffls.fillna(0.0,inplace=True)

# thresholds = [x-0.03 for x in ffls_normalized.mean()]
# plt.plot(emg_fsr_time,ffls_normalized)
# for i in range(6):
#     plt.subplot(3,2,i+1)
#     plt.axhline(y=thresholds[i], color='r', linestyle='-') 
#     plt.plot(emg_fsr_time,ffls_normalized.iloc[:,i])
    # plt.hist(ffls_normalized.iloc[:,i],50)

plt.plot(emg_fsr_time,mov_avg_ffls)
colors=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
for i in range(1,7):
  for idx in press_locations(mov_avg_ffls,i):
    plt.axvline(x=idx,linestyle='-',color=colors[i])
plt.show()