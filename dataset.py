from extraction_util import get_mins, get_min, get_datapoints, make_dataset

data_dict=[
    {
        'root':'P_1',
        'idx':'2'
    },
    {
        'root':'P_2',
        'idx':'3'
    },
    {
        'root':'P_3',
        'idx':'1'
    },
    {
        'root':'P_4',
        'idx':['0','1']
    },
    {
        'root':'P_5',
        'idx':['0','1']
    },
    {
        'root':'P_6',
        'idx':['0','1']
    },
    {
        'root':'P_7',
        'idx':['0','3']
    },
    {
        'root':'P_8',
        'idx':['4','5']
    },
    {
        'root':'P_9',
        'idx':['0','1']
    },
    {
        'root':'P_10',
        'idx':['0','1']
    }
]
mins=get_mins(data_dict)
max_length=get_min(mins)
print(f"Clipping to {max_length} samples")
print("Collecting Datapoints")
datapoints=get_datapoints(data_dict,max_length)
print(f"Number of Datapoints:{len(datapoints)}")
print("Generating Dataset")
dataset=make_dataset(datapoints)
print(dataset.info())
print(dataset.head())
dataset.to_csv("dataset.csv")
print("Saved to dataset.csv")