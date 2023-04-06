import torch
import numpy as _np
import pandas as _pd

def to_reshaped_tensor(test_input):
    return test_input.reshape(len(test_input),1,311,10)

def _normalize(data):
    return (data-_np.min(data))/(_np.max(data)-_np.min(data))

def _standardize(array):
  mean = _np.mean(array, axis=0)
  std = _np.std(array, axis=0)
  array = (array - mean) / std
  return array

def preprocess(data_list:list):
    df = _pd.DataFrame(data_list,columns=["FSR1","FSR2","FSR3","FSR4","FSR5","FSR6"])
    print(df.shape)
    df[["FSR7","FSR8","FSR9","FSR10"]] = 0.0
    print(df.shape)
    df = df.apply(_normalize)
    df = _standardize(df)
    return df

def torch_argmax(tensor):
    return torch.argmax(tensor)