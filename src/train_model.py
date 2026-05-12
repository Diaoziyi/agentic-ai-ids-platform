import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib
import os

# -------------------------------------------------------
# Step 1: Load NSL-KDD dataset
# -------------------------------------------------------

DATA_PATH = "data/nsl-kdd/"

train_file = os.path.join(DATA_PATH, "KDDTrain+.txt")
test_file = os.path.join(DATA_PATH, "KDDTest+.txt")

column_names = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root","num_file_creations",
    "num_shells","num_access_files","num_outbound_cmds","is_host_login",
    "is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
    "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
    "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"
]

print("Loading dataset...")
df_train = pd.read_csv(train_file, names=column_names)
df_test = pd.read_csv(test_file, names=column_names)

# remove difficulty column
df_train = df_train.drop("difficulty", axis=1)
df_test = df_test.drop("difficulty", axis=1)

# simplify attack labels
def simplify(label):
    if label == "normal":
        return "normal"
    else:
        return "attack"

df_train["binary_label"] = df_train["label"].apply(simplify)
df_test["binary_label"] = df_test["label"].apply(simplify)

# -------------------------------------------------------
# Step 2: Preprocessing
# -------------------------------------------------------

categorical_cols = ["protocol_type", "service", "flag"]
numeric_cols = [col for col in df_train.columns if col not in categorical_cols + ["label","binary_label"]]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

# -------------------------------------------------------
# Step 3: Build ML model
# -------------------------------------------------------

model = RandomForestClassifier(
    n_estimators=120,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

clf = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("model", model)
])

# -------------------------------------------------------
# Step 4: Train and Evaluate
# -------------------------------------------------------

X_train = df_train.drop(["label","binary_label"], axis=1)
y_train = df_train["binary_label"]

X_test = df_test.drop(["label","binary_label"], axis=1)
y_test = df_test["binary_label"]

print("Training model...")
clf.fit(X_train, y_train)

print("Evaluating model...")
y_pred = clf.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -------------------------------------------------------
# Step 5: Save Model
# -------------------------------------------------------

os.makedirs("models", exist_ok=True)
joblib.dump(clf, "models/ids_model.pkl")

print("\nModel saved as models/ids_model.pkl")
