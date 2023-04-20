import pandas as pd
import matplotlib.pyplot as plt

def get_len(string):
    print(string.split())
    return len(string.split())

df = pd.read_csv("combined/new_dataset.csv",header=0)
df.info()
data_len_df=pd.DataFrame(df.iloc[0:2,2].apply(get_len))
# print(len(df['data'][0]))
# plt.hist(df['stim'],bins=7)
data_len_df.info()
plt.hist(data_len_df,bins=3)
plt.show()
print(data_len_df.data.unique())