import numpy as np
import pandas as pd

def _normalize(data):
    return (data-data.min())/(data.max()-data.min())

def _standardize(array):
  mean = np.mean(array, axis=0)
  std = np.std(array, axis=0)
  array = (array - mean) / std
  return array

def get_mins(data_dict:[{'root':str,'idx':[str]}])->[{'root':str,'idx':str,'min':int}]:
    mins=[]
    for folder in data_dict:
        root=folder['root']
        indices=folder['idx']
        print(f"\nProcessing Folder: {root}",end='\t')
        for idx in indices:
            print(f"Index:{idx}",end='\t')
            stim=pd.read_csv(f"data/{root}/stim{idx}.txt",header=None)
            good_stim=stim.iloc[:,:7]
            good_stim.columns=['key','F1','F2','F3','F4','F5','F6']
            
            data=[]
            for i in range(1,7):
                # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-where-column-matches-certain-value
                indices=np.where(good_stim[f'F{i}']>0.0)[0]
                temp_data=good_stim.iloc[list(indices)].copy(deep=True)
                # https://stackoverflow.com/questions/29517072/add-column-to-dataframe-with-constant-value
                temp_data['Stim']=i
                temp_data=temp_data.drop(columns=['F1','F2','F3','F4','F5','F6'])
                data.append(temp_data)
            
            good_data=pd.concat(data)
            good_data.sort_values('key',inplace=True)
            
            good_data['group'] = good_data['Stim'].ne(good_data['Stim'].shift()).cumsum()
            grouped_data = good_data.groupby('group')

            mins.append({'root':root,'idx':idx,'min':min([data.shape[0] for name,data in grouped_data])})
    print()
    return mins

def get_min(mins:[{'root':str,'idx':str,'min':int}])->int:
    return min([x['min'] for x in mins])

def get_datapoints():
    datapoints=[]
    # Read Dataset
    dataset=pd.read_csv(f"combined/emg_fsr_data.csv",header=0)
    
    # FSR Data is first 11 columns of Dataset
    good_fsr=dataset.iloc[:,:11]
    good_fsr.columns=['key','FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']
    
    # FFLS Data is last 6 columns
    ffls_data=dataset.iloc[:,21:]
    mov_avg_ffls = ffls_data.rolling(20).mean()
    ffls_data = mov_avg_ffls.fillna(0.0)
    ffls_data.columns=['Fing1','Fing2','Fing3','Fing4','Fing5','Fing6'] # Renaming Columns
    
    # Standardize and Normalize FFLS Data
    ffls_standardized = _standardize(ffls_data) 
    ffls_normalized = _normalize(ffls_data)
    
    # Copying Key column to FFLS Data
    ffls_normalized['key']=good_fsr['key']
    # Reordering columns
    ffls_normalized=ffls_normalized[['key','Fing1','Fing2','Fing3','Fing4','Fing5','Fing6']]
    # Calculate Thresholds
    thresholds = [x-0.03 for x in ffls_normalized.mean()]
    
    data=[]
    for i in range(1,7):
        # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-where-column-matches-certain-value
        # Find where Finger is pressed
        indices=np.where(ffls_normalized[f'Fing{i}']<thresholds[i])[0]
        # Isolate those samples
        temp_data=ffls_normalized.iloc[list(indices)].copy(deep=True)
        # https://stackoverflow.com/questions/29517072/add-column-to-dataframe-with-constant-value
        temp_data['Stim']=i
        temp_data=temp_data.drop(columns=['Fing1','Fing2','Fing3','Fing4','Fing5','Fing6'])
        data.append(temp_data)
    
    good_data=pd.concat(data)
    good_data.sort_values('key',inplace=True)
    print("Grouping")
    good_data['group'] = good_data['Stim'].ne(good_data['Stim'].shift()).cumsum()
    grouped_data = good_data.groupby('group')
    good_datas = []
    for name, data in grouped_data:
        good_datas.append(data.drop(columns=['group']))
    
    lengths = [data.shape[0] for name,data in grouped_data]
    lengths = [x for x in lengths if x>=100]
    max_length = min(lengths)
    if max_length%2 !=0:
        max_length-=1
    print(f"Max Length: {max_length} Datapoints above: {len([x for x in lengths if x>=max_length])}")
    
    # Merge in FSR Data
    for data in good_datas:
        if len(data)>=max_length:
            temp_data = data.iloc[:max_length,:].merge(good_fsr,how='inner',on=['key'])
            if temp_data.shape != (max_length,12):
                input(f"{temp_data.shape} cont?")
            datapoints.append(temp_data)
    # # return
    # for data in better_data:
    #     if len(data)>=max_length:
    #         datapoints.append(data.iloc[:max_length,:])
    print()
    return datapoints

def get_blanks(max_length=90):
    datapoints=[]
            
    dataset=pd.read_csv(f"combined/emg_fsr_data.csv",header=0)
    ffls_data=dataset.iloc[:,21:]
    ffls_data.columns=['Fing1','Fing2','Fing3','Fing4','Fing5','Fing6']
    
    good_fsr=dataset.iloc[:,:11]
    good_fsr.columns=['key','FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']
    ffls_data['key']=good_fsr['key']
    ffls_data=ffls_data[['key','Fing1','Fing2','Fing3','Fing4','Fing5','Fing6']]
    ffls_standardized = _standardize(ffls_data)
    ffls_normalized = _normalize(ffls_data)
    thresholds = [x-0.03 for x in ffls_normalized.mean()]
    all_sets=[]
    for i in range(1,7):
        # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-where-column-matches-certain-value
        indices=set(np.where(ffls_normalized[f'Fing{i}']>thresholds[i])[0])
        all_sets.append(indices)
    indices_intersection = set.intersection(*all_sets)
    good_data=ffls_data.iloc[list(indices_intersection)].copy(deep=True)
    # https://stackoverflow.com/questions/29517072/add-column-to-dataframe-with-constant-value
    good_data['Stim']=0
    good_data=good_data.drop(columns=['Fing1','Fing2','Fing3','Fing4','Fing5','Fing6'])
    good_data.sort_values('key',inplace=True)
    
    good_datas = [good_data.iloc[i:i+max_length,:] for i in range(0, len(good_data),max_length)]
    
    # Merge in FSR Data
    for data in good_datas:
        if len(data)==max_length:
            temp_data = data.iloc[:max_length,:].merge(good_fsr,how='inner',on=['key'])
            if temp_data.shape != (max_length,12):
                input(f"{temp_data.shape} cont?")
            datapoints.append(temp_data)
    print()
    return datapoints

def get_datapoints_with_ffls(data_dict:[{'root':str,'idx':[str]}],max_length=311):
    datapoints=[]
    for folder in data_dict:
        root=folder['root']
        indices=folder['idx']
        print(f"\nProcessing Folder: {root}",end='\t')
        for idx in indices:
            print(f"Index:{idx}",end='\t')
            stim=pd.read_csv(f"data/{root}/stim{idx}.txt",header=None)
            good_stim=stim.iloc[:,:7]
            good_stim.columns=['key','Fing1','Fing2','Fing3','Fing4','Fing5','Fing6']
            
            emg=pd.read_csv(f"data/{root}/unfiltered_emg{idx}.txt",header=None)
            emg.columns=['key','FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10','FFLS1','FFLS2','FFLS3','FFLS4','FFLS5','FFLS6']
            fsr_data=emg.iloc[:,:11]
            ffls_data=emg.loc[:,['key','FFLS1','FFLS2','FFLS3','FFLS4','FFLS5','FFLS6']]

            data=[]
            for i in range(1,7):
                # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-where-column-matches-certain-value
                indices=np.where(good_stim[f'Fing{i}']>0.0)[0]
                temp_data=good_stim.iloc[list(indices)].copy(deep=True)
                # https://stackoverflow.com/questions/29517072/add-column-to-dataframe-with-constant-value
                temp_data['Stim']=i
                temp_data=temp_data.drop(columns=['Fing1','Fing2','Fing3','Fing4','Fing5','Fing6'])
                data.append(temp_data)
            
            good_data=pd.concat(data)
            good_data.sort_values('key',inplace=True)
            
            good_data['group'] = good_data['Stim'].ne(good_data['Stim'].shift()).cumsum()
            grouped_data = good_data.groupby('group')
            good_datas = []
            for name, data in grouped_data:
                good_datas.append(data.drop(columns=['group']))
            
            better_data=[]
            # Merge in FSR and FFLS Data
            for data in good_datas:
                better_data.append(data.merge(fsr_data,how='inner',on=['key']).merge(ffls_data,how='inner',on=['key']))
            
            if max_length!=None:
                for data in better_data:
                    datapoints.append(data.iloc[:max_length,:])
            else:
                for data in better_data:
                    datapoints.append(data)
    print()
    return datapoints

def make_dataset(datapoints:[pd.DataFrame])->pd.DataFrame:
    processed_datadicts=[]
    for data in datapoints:
        stim=data['Stim'][0]
        input(f"{data.iloc[:,2:].shape} cont?")
        array_2D=data.loc[:,['FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']].to_numpy().transpose().flatten().tolist()
        processed_datadicts.append({
            'stim':stim,
            'data':' '.join(str(x) for x in array_2D)
        })
    dataset=pd.DataFrame(processed_datadicts)
    return dataset

def make_dataset_with_blanks(datapoints:[pd.DataFrame],datapoints_blank:[pd.DataFrame])->pd.DataFrame:
    processed_datadicts=[]
    for data in datapoints:
        stim=data['Stim'][0]
        array_2D=data.loc[:,['FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']].to_numpy().transpose().flatten().tolist()
        processed_datadicts.append({
            'stim':stim,
            'data':' '.join(str(x) for x in array_2D)
        })
    for data in datapoints_blank:
        stim=data['Stim'][0]
        array_2D=data.loc[:,['FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']].to_numpy().transpose().flatten().tolist()
        processed_datadicts.append({
            'stim':stim,
            'data':' '.join(str(x) for x in array_2D)
        })
    dataset=pd.DataFrame(processed_datadicts)
    return dataset

def make_dataset_with_ffls(datapoints:[pd.DataFrame])->pd.DataFrame:
    processed_datadicts=[]
    for data in datapoints:
        stim=data['Stim'][0]
        array_2D_fsr=data.loc[:,['FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']].to_numpy()
        array_2D_ffls=data.loc[:,['FFLS1','FFLS2','FFLS3','FFLS4','FFLS5','FFLS6']].to_numpy()
        processed_datadicts.append({
            'stim':stim,
            'fsr_data':array_2D_fsr,
            'ffls_data':array_2D_ffls
        })
    dataset=pd.DataFrame(processed_datadicts)
    return dataset

print("Collecting Datapoints")
datapoints = get_datapoints()
print(f"No. of Datapoints: {len(datapoints)}\n")
blank_length = int(input("Enter max_length: "))
print("Collecting Blanks")
blanks = get_blanks(blank_length)
print(f"No. of Blanks: {len(blanks)}\n")

print("Making Dataset - Without Blanks")
generated_dataset = make_dataset(datapoints)
print(generated_dataset.head())
generated_dataset.to_csv("combined/new_dataset.csv")
print("Saved to new_dataset.csv\n")

print("Making Dataset - With Blanks")
generated_dataset = make_dataset_with_blanks(datapoints,blanks)
print(generated_dataset.head())
generated_dataset.to_csv("combined/new_dataset_with_blanks.csv")
print("Saved to new_dataset_with_blanks.csv")