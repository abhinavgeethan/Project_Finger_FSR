from scipy.io import loadmat
import pandas as pd

mat = loadmat('emg_fsr_data.mat')
data = pd.DataFrame(mat['emg_fsr_data'])
data.to_csv("emg_fsr_data.csv")