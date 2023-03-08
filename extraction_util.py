import numpy as np
import pandas as pd

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
            
            good_time=pd.read_csv(f"data/{root}/timestamp{idx}.txt",header=None)
            
            good_data=pd.merge(good_time,good_stim, on=[0])
            good_data.columns=['key','timestamp','F1','F2','F3','F4','F5','F6']
            data=[]
            for i in range(1,7):
                # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-where-column-matches-certain-value
                indices=np.where(good_data[f'F{i}']>0.0)[0]
                temp_data=good_data.iloc[list(indices)].copy(deep=True)
                # https://stackoverflow.com/questions/29517072/add-column-to-dataframe-with-constant-value
                temp_data['Stim']=i
                data.append(temp_data)
            
            great_data=pd.concat(data)
            great_data.sort_values('key',inplace=True)
            
            great_data['group'] = great_data['Stim'].ne(great_data['Stim'].shift()).cumsum()
            grouped_data = great_data.groupby('group')
            great_datas = []
            for name, data in grouped_data:
                great_datas.append(data.drop(columns=['F1','F2','F3','F4','F5','F6','group']))
            
            mins.append({'root':root,'idx':idx,'min':min([x.shape[0] for x in great_datas])})
    print()
    return mins

def get_min(mins:[{'root':str,'idx':str,'min':int}])->int:
    return min([x['min'] for x in mins])

def get_datapoints(data_dict:[{'root':str,'idx':[str]}],max_length=311):
    datapoints=[]
    for folder in data_dict:
        root=folder['root']
        indices=folder['idx']
        print(f"\nProcessing Folder: {root}",end='\t')
        for idx in indices:
            print(f"Index:{idx}",end='\t')
            stim=pd.read_csv(f"data/{root}/stim{idx}.txt",header=None)
            good_stim=stim.iloc[:,:7]
            
            emg=pd.read_csv(f"data/{root}/emg{idx}.txt",header=None)
            good_emg=emg.iloc[:,:11]
            good_emg.columns=['key','FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']

            good_time=pd.read_csv(f"data/{root}/timestamp{idx}.txt",header=None)
            
            good_data=pd.merge(good_time,good_stim, on=[0])
            good_data.columns=['key','timestamp','F1','F2','F3','F4','F5','F6']
            data=[]
            for i in range(1,7):
                # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-where-column-matches-certain-value
                indices=np.where(good_data[f'F{i}']>0.0)[0]
                temp_data=good_data.iloc[list(indices)].copy(deep=True)
                # https://stackoverflow.com/questions/29517072/add-column-to-dataframe-with-constant-value
                temp_data['Stim']=i
                data.append(temp_data)
            
            great_data=pd.concat(data)
            great_data.sort_values('key',inplace=True)
            
            great_data['group'] = great_data['Stim'].ne(great_data['Stim'].shift()).cumsum()
            grouped_data = great_data.groupby('group')
            great_datas = []
            for name, data in grouped_data:
                great_datas.append(data.drop(columns=['F1','F2','F3','F4','F5','F6','group','timestamp']))
            
            better_data=[]
            # Merge in FSR Data
            for data in great_datas:
                better_data.append(data.merge(good_emg,how='inner',on=['key']))
            
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
        array_2D=data.loc[:,['FSR1','FSR2','FSR3','FSR4','FSR5','FSR6','FSR7','FSR8','FSR9','FSR10']].to_numpy()
        processed_datadicts.append({
            'stim':stim,
            'data':array_2D
        })
    dataset=pd.DataFrame(processed_datadicts)
    return dataset