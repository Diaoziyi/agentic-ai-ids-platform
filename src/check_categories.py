import pandas as pd

df = pd.read_csv("data/nsl-kdd/KDDTrain+.txt", header=None)

print("protocol_type unique values:", df[1].unique()[:20])
print("service unique values:", df[2].unique()[:20])
print("flag unique values:", df[3].unique()[:20])
