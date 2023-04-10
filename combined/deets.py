import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("combined/new_dataset.csv",header=0)
df.info()
print(len(df['data'][0]))
plt.hist(df['stim'],bins=7)
plt.show()