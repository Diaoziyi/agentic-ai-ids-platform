import pandas as pd

df_train = pd.read_csv("data/nsl-kdd/KDDTrain+.txt", header=None)
df_test = pd.read_csv("data/nsl-kdd/KDDTest+.txt", header=None)

# 标签是最后一列
train_labels = df_train.iloc[:, -1].unique()
test_labels = df_test.iloc[:, -1].unique()

print("Train labels:", train_labels)
print("Test labels:", test_labels)
print("Total unique:", set(train_labels) | set(test_labels))
