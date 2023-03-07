import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

root="20012014"
idx='0'

stim=pd.read_csv(f"{root}/stim{idx}.txt",header=None)
# stim_activation=pd.read_csv(f"{root}/stim_activation{idx}.txt",header=None)
time=pd.read_csv(f"{root}/timestamp{idx}.txt",header=None)
emg=pd.read_csv(f"{root}/emg{idx}.txt",header=None)

emg[0].apply(int)
good_emg=emg.iloc[:,:11]
good_emg.columns=['key','FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']
# print(good_emg.head())

good_time=time
good_stim=stim.iloc[:,:7]
good_data=pd.merge(good_time,good_stim, on=[0])
good_data.columns=['key','timestamp','F1','F2','F3','F4','F5','F6']
# print(good_data.head())

data=[]
for i in range(1,7):
    # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-where-column-matches-certain-value
    indices=np.where(good_data[f'F{i}']==1.0)[0]
    temp_data=good_data.iloc[list(indices)]
    # https://stackoverflow.com/questions/29517072/add-column-to-dataframe-with-constant-value
    temp_data['Stim']=i
    data.append(temp_data)

print([x.shape[0] for x in data])
# https://stackoverflow.com/questions/44327999/how-to-merge-multiple-dataframes
great_data=pd.concat(data)
great_data.sort_values('key',inplace=True)
print(great_data.head())

# https://stackoverflow.com/questions/64163984/how-to-split-a-dataframe-each-time-a-string-value-changes-in-a-column
great_data['group'] = great_data['Stim'].ne(great_data['Stim'].shift()).cumsum()
grouped_data = great_data.groupby('group')
great_datas = []
for name, data in grouped_data:
    great_datas.append(data.drop(columns=['F1','F2','F3','F4','F5','F6','group']))
better_data=[]
for data in great_datas:
    better_data.append(data.merge(good_emg,how='inner',on=['key']))

# print(great_datas)
print(f"Min:{min([x.shape[0] for x in great_datas])} | Max:{max([x.shape[0] for x in great_datas])}")
print("Shapes")
print([x.shape[0] for x in great_datas])
print(f"No: {len(great_datas)}")
# plt.subplot(2,1,1)
# plt.plot(good_time.iloc[:,1], good_stim.iloc[:,1:])
# plt.subplot(2,1,2)
# plt.plot(good_time.iloc[:,1], stim_activation.iloc[:,1])
# plt.plot(great_data['timestamp'], great_data.iloc[:,2:7])
# plt.axvline(first_pulse_end,color='g',linestyle='--')
# plt.axvline(last_pulse_start,color='g',linestyle='--')
# plt.plot(good_time, derivative)
for i in range(6):
    plt.subplot(3,2,i+1)
    plt.plot(good_time.iloc[:,1], good_stim.iloc[:,i+1])

plt.show()