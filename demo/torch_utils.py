import torch
import numpy as _np

NUM_TIMESTEPS = 0
NUM_SENSORS = 0

def to_CNN_reshaped_tensor(test_input:_np.ndarray,NUM_TIMESTEPS:int,NUM_SENSORS:int)->torch.Tensor:
    return torch.tensor(test_input.reshape(1,NUM_TIMESTEPS,NUM_SENSORS))

def to_LSTM_reshaped_tensor(test_input:_np.ndarray,NUM_TIMESTEPS:int,NUM_SENSORS:int)->torch.Tensor:
    return torch.tensor(test_input.reshape(NUM_TIMESTEPS,NUM_SENSORS))

def _normalize(data):
    return (data-_np.min(data))/(_np.max(data)-_np.min(data))

def _standardize(array):
  mean = _np.mean(array, axis=0)
  std = _np.std(array, axis=0)
  array = (array - mean) / std
  return array

def _load_and_normalize(data):
    split_data=[]
    for row in data:
        row=_np.array(row.split(',')).astype('float32')
        row = _normalize(row)
        split_data.append(row)
    data=_np.reshape(split_data,(NUM_TIMESTEPS,NUM_SENSORS))
    return data

def preprocess(data_list:list,num_timesteps:int,num_sensors:int)->_np.ndarray:
    global NUM_TIMESTEPS, NUM_SENSORS
    NUM_TIMESTEPS = num_timesteps
    NUM_SENSORS = num_sensors
    df = _load_and_normalize(data_list)
    df = _np.stack(df,axis=0)
    df = _standardize(df)
    return df

def torch_argmax(tensor:torch.Tensor)->int:
    return torch.argmax(tensor.unsqueeze(0)).item()