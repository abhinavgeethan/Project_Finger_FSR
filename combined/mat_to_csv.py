from scipy.io import loadmat
import pandas as pd

mat = loadmat('combined/emg_fsr_data.mat')
data = pd.DataFrame(mat['emg_fsr_data'])
data.to_csv("combined/emg_fsr_data.csv")