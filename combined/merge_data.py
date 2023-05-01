import pandas as pd

path_1 = "combined/Our_dataset_with_blanks.csv"
path_2 = "combined/Our_dataset_with_blanks_2.csv"
df1 = pd.read_csv(path_1,header=0)
print(f"Loaded {path_1}: {df1.shape}")
df2 = pd.read_csv(path_2,header=0)
print(f"Loaded {path_2}: {df2.shape}")

merged = pd.concat([df1.iloc[:,1:],df2.iloc[:,1:]])
print(merged.info())
print(merged.head())
merged.to_csv("combined/Our_padded_combined_with_blanks.csv")
print("Saved to combined/Our_padded_combined_with_blanks.csv")