import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def _normalize(data):
    return (data-data.min())/(data.max()-data.min())

def _standardize(array):
  mean = np.mean(array, axis=0)
  std = np.std(array, axis=0)
  array = (array - mean) / std
  return array

def get_datapoints(file_path):
    datapoints=[]
    # Read Dataset
    dataset=pd.read_csv(file_path,header=0)
    
    # FSR Data is first 11 columns of Dataset
    good_fsr=dataset.iloc[:,:7]
    good_fsr.columns=['key','FSR1','FSR2','FSR3','FSR4','FSR5','FSR6']

    good_stim = pd.DataFrame(dataset.iloc[:,7]).astype(int)
    good_stim.columns=['stim']
    good_stim['key'] = dataset['key']
    good_stim = good_stim[['key','stim']]
    good_stim = good_stim [good_stim.stim >0]
    input(f"Stims: {good_stim.stim.unique()} cont?")
    
    print("Grouping")
    good_stim['group'] = good_stim['stim'].ne(good_stim['stim'].shift()).cumsum()
    grouped_data = good_stim.groupby('group')
    good_datas = []
    for name, data in grouped_data:
        good_datas.append(data.drop(columns=['group']))
    
    lengths = [data.shape[0] for name,data in grouped_data]
    lengths.sort(reverse=True)
    print(lengths)
    limit = int(input("threshold?"))
    lengths = [x for x in lengths if x>=limit]
    max_length = min(lengths)
    if max_length%2 !=0:
        max_length-=1
    print(f"Max Length: {max_length} Datapoints above: {len([x for x in lengths if x>=max_length])}")
    
    # Merge in FSR Data
    for data in good_datas:
        if len(data)>=max_length:
            temp_data = data.iloc[:max_length,:].merge(good_fsr,how='inner',on=['key'])
            if temp_data.shape != (max_length,8):
                input(f"{temp_data.shape} cont?")
            datapoints.append(temp_data)
    # # return
    # for data in better_data:
    #     if len(data)>=max_length:
    #         datapoints.append(data.iloc[:max_length,:])
    print()
    return datapoints

def get_padded_datapoints(file_path):
    datapoints=[]
    # Read Dataset
    dataset=pd.read_csv(file_path,header=0)
    
    # FSR Data is first 11 columns of Dataset
    good_fsr=dataset.iloc[:,:7]
    good_fsr.columns=['key','FSR1','FSR2','FSR3','FSR4','FSR5','FSR6']

    good_stim = pd.DataFrame(dataset.iloc[:,7]).astype(int)
    good_stim.columns=['stim']
    good_stim['key'] = dataset['key']
    good_stim = good_stim[['key','stim']]
    good_stim = good_stim [good_stim.stim >0]
    input(f"Stims: {good_stim.stim.unique()} cont?")
    
    mid_indexes_keys = []
    print("Grouping")
    good_stim['group'] = good_stim['stim'].ne(good_stim['stim'].shift()).cumsum()
    grouped_data = good_stim.groupby('group')
    good_datas = []
    for name, data in grouped_data:
        if data.shape[0]>20:
            good_datas.append(data.drop(columns=['group']))
            mid_indexes_keys.append(data.iloc[data.shape[0]//2,0])
    
    lengths = [data.shape[0] for _,data in grouped_data]
    lengths.sort(reverse=True)
    print(lengths)
    max_length = int(input("Size?"))
    if max_length%2 !=0:
        max_length-=1
    print(f"Max Length: {max_length}")
    
    # Merge in FSR Data
    for k in mid_indexes_keys:
        where = np.where(good_stim.key == k)[0][0]
        temp_data = good_stim.iloc[max(where-(max_length//2),0):min(where+(max_length//2),good_stim.shape[0]),:].drop(columns=['group']).merge(good_fsr,how='inner',on=['key'])
        temp_data.stim = good_stim[good_stim.key==k].stim.iloc[0]
        if temp_data.shape[0]==max_length:
            datapoints.append(temp_data)
  
    print()
    return datapoints

def get_blanks(file_path, max_length=46):
    datapoints=[]
    # Read Dataset
    dataset=pd.read_csv(file_path,header=0)
    
    # FSR Data is first 11 columns of Dataset
    good_fsr=dataset.iloc[:,:7]
    good_fsr.columns=['key','FSR1','FSR2','FSR3','FSR4','FSR5','FSR6']

    good_stim = pd.DataFrame(dataset.iloc[:,7]).astype(int)
    good_stim.columns=['stim']
    good_stim['key'] = dataset['key']
    good_stim = good_stim[['key','stim']]
    good_stim = good_stim [good_stim.stim ==0]
    input(f"Stims {good_stim.stim.unique()} cont?")
    
    good_datas = [good_stim.iloc[i:i+max_length,:] for i in range(0, len(good_stim),max_length)]
    
    # Merge in FSR Data
    for data in good_datas:
        if len(data)==max_length:
            temp_data = data.iloc[:max_length,:].merge(good_fsr,how='inner',on=['key'])
            if temp_data.shape != (max_length,8):
                input(f"{temp_data.shape} cont?")
            datapoints.append(temp_data)
    print()
    return datapoints

def make_dataset(datapoints:[pd.DataFrame])->pd.DataFrame:
    processed_datadicts=[]
    for data in datapoints:
        stim=data['stim'][0]
        array_2D=data.loc[:,['FSR1','FSR2','FSR3','FSR4','FSR5','FSR6']].to_numpy().transpose().flatten().tolist()
        processed_datadicts.append({
            'stim':stim,
            'data':' '.join(str(x) for x in array_2D)
        })
    dataset=pd.DataFrame(processed_datadicts)
    return dataset

def make_dataset_with_blanks(datapoints:[pd.DataFrame],datapoints_blank:[pd.DataFrame])->pd.DataFrame:
    processed_datadicts=[]
    for data in datapoints:
        stim=data['stim'][0]
        array_2D=data.loc[:,['FSR1','FSR2','FSR3','FSR4','FSR5','FSR6']].to_numpy().transpose().flatten().tolist()
        processed_datadicts.append({
            'stim':stim,
            'data':' '.join(str(x) for x in array_2D)
        })
    for data in datapoints_blank:
        stim=data['stim'][0]
        array_2D=data.loc[:,['FSR1','FSR2','FSR3','FSR4','FSR5','FSR6']].to_numpy().transpose().flatten().tolist()
        processed_datadicts.append({
            'stim':stim,
            'data':' '.join(str(x) for x in array_2D)
        })
    dataset=pd.DataFrame(processed_datadicts)
    return dataset

file_path = "combined/data.csv"
print("Collecting Datapoints")
datapoints = get_padded_datapoints(file_path)
print(f"No. of Datapoints: {len(datapoints)}\n")
blank_length = int(input("Enter max_length: "))
print("Collecting Blanks")
blanks = get_blanks(file_path,blank_length)
print(f"No. of Blanks: {len(blanks)}\n")

print("Making Dataset - Without Blanks")
generated_dataset = make_dataset(datapoints)
print(generated_dataset.head())
generated_dataset.to_csv("combined/Our_dataset_2.csv")
print("Saved to Our_dataset.csv\n")

print("Making Dataset - With Blanks")
generated_dataset = make_dataset_with_blanks(datapoints,blanks)
print(generated_dataset.head())
generated_dataset.to_csv("combined/Our_dataset_with_blanks_2.csv")
print("Saved to Our_dataset_with_blanks.csv")